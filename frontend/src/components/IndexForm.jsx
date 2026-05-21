import { useState } from "react";
import { postCollectionIndex } from "../api";
import DocumentList from "./DocumentList";
import FileUpload from "./FileUpload";

export default function IndexForm({ settings, collectionName, indexStatus, onIndexed }) {
  const [showFolder, setShowFolder] = useState(false);
  const [folderPath, setFolderPath] = useState("./sample-docs");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [docRefresh, setDocRefresh] = useState(0);

  const handleIndex = async () => {
    setLoading(true);
    setError(null);
    setStats(null);
    try {
      const result = await postCollectionIndex(collectionName, {
        folderPath,
        chunkSize: settings.chunkSize,
        chunkOverlap: settings.chunkOverlap,
        embedModel: settings.embedModel,
      });
      setStats(result);
      setDocRefresh((n) => n + 1);
      onIndexed(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleUploaded = () => {
    setDocRefresh((n) => n + 1);
    onIndexed({ chunks_created: -1 });
  };

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-5">
      <h2 className="font-semibold text-base mb-3">
        {indexStatus?.indexed ? "Documents" : "Step 2: Add documents"}
      </h2>

      {/* File upload */}
      <FileUpload collectionName={collectionName} onUploaded={handleUploaded} />

      {/* Folder indexing (advanced) */}
      <div className="mt-3">
        <button
          onClick={() => setShowFolder(!showFolder)}
          className="text-xs text-gray-500 hover:text-gray-700"
        >
          {showFolder ? "Hide" : "Or index a folder..."}
        </button>
        {showFolder && (
          <div className="flex gap-2 mt-2">
            <input
              type="text"
              value={folderPath}
              onChange={(e) => setFolderPath(e.target.value)}
              placeholder="Path to folder"
              className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={handleIndex}
              disabled={loading || !folderPath}
              className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed shrink-0"
            >
              {loading ? "Indexing..." : "Index"}
            </button>
          </div>
        )}
      </div>

      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      {stats && stats.chunks_created >= 0 && (
        <p className="mt-2 text-sm text-green-700">
          Indexed {stats.files_loaded} files ({stats.chunks_created} chunks) in {stats.time_seconds}s
        </p>
      )}

      {/* Document list */}
      <DocumentList collectionName={collectionName} refreshKey={docRefresh} />
    </section>
  );
}
