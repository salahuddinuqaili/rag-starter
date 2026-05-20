import { useState } from "react";
import { postIndex } from "../api";

export default function IndexForm({ settings, indexStatus, onIndexed }) {
  const [folderPath, setFolderPath] = useState("./sample-docs");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);

  const handleIndex = async () => {
    setLoading(true);
    setError(null);
    setStats(null);
    try {
      const result = await postIndex({
        folderPath,
        chunkSize: settings.chunkSize,
        chunkOverlap: settings.chunkOverlap,
        dbPath: settings.dbPath,
        embedModel: settings.embedModel,
      });
      setStats(result);
      onIndexed(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-5">
      <h2 className="font-semibold text-base mb-3">
        {indexStatus?.indexed ? "Documents indexed" : "Step 2: Index your documents"}
      </h2>

      {indexStatus?.indexed && !stats && (
        <p className="text-sm text-gray-600 mb-3">
          Index contains {indexStatus.chunk_count} chunks. You can re-index below.
        </p>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={folderPath}
          onChange={(e) => setFolderPath(e.target.value)}
          placeholder="Path to your documents folder"
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

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}

      {stats && (
        <p className="mt-2 text-sm text-green-700">
          Indexed {stats.files_loaded} files ({stats.chunks_created} chunks) in{" "}
          {stats.time_seconds}s
        </p>
      )}
    </section>
  );
}
