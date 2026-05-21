import { useEffect, useState } from "react";
import { deleteDocument, fetchDocuments } from "../api";

export default function DocumentList({ collectionName, refreshKey }) {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    fetchDocuments(collectionName).then(setDocs).catch(() => setDocs([]));
  }, [collectionName, refreshKey]);

  const handleDelete = async (source) => {
    await deleteDocument(collectionName, source);
    setDocs((prev) => prev.filter((d) => d.source !== source));
  };

  if (docs.length === 0) return null;

  return (
    <div className="mt-3">
      <h3 className="text-xs font-medium text-gray-500 mb-2 uppercase tracking-wide">
        Indexed documents
      </h3>
      <div className="border border-gray-200 rounded-md divide-y divide-gray-100">
        {docs.map((d) => (
          <div key={d.source} className="flex items-center justify-between px-3 py-2 text-sm">
            <div>
              <span className="text-gray-800">{d.source}</span>
              <span className="text-gray-400 ml-2 text-xs">{d.chunk_count} chunks</span>
            </div>
            <button
              onClick={() => handleDelete(d.source)}
              className="text-gray-300 hover:text-red-500 text-xs"
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
