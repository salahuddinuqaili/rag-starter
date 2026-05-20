export default function Settings({ settings, setSettings, indexStatus, onClose }) {
  const update = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <aside className="w-72 border-l border-gray-200 bg-white p-5 shrink-0 overflow-y-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-sm">Settings</h2>
        <button onClick={onClose} className="text-gray-400 hover:text-gray-600 text-lg">
          &times;
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Chunk size (characters)
          </label>
          <input
            type="number"
            min={100}
            max={2000}
            step={50}
            value={settings.chunkSize}
            onChange={(e) => update("chunkSize", Number(e.target.value))}
            className="w-full border border-gray-300 rounded-md px-2 py-1.5 text-sm"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">
            Results to retrieve (top-k)
          </label>
          <input
            type="number"
            min={1}
            max={20}
            value={settings.topK}
            onChange={(e) => update("topK", Number(e.target.value))}
            className="w-full border border-gray-300 rounded-md px-2 py-1.5 text-sm"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">LLM model</label>
          <input
            type="text"
            value={settings.model}
            onChange={(e) => update("model", e.target.value)}
            className="w-full border border-gray-300 rounded-md px-2 py-1.5 text-sm"
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-600 mb-1">Database path</label>
          <input
            type="text"
            value={settings.dbPath}
            onChange={(e) => update("dbPath", e.target.value)}
            className="w-full border border-gray-300 rounded-md px-2 py-1.5 text-sm"
          />
        </div>

        {indexStatus && (
          <div className="pt-2 border-t border-gray-200 text-xs text-gray-500">
            {indexStatus.indexed ? (
              <p>Index: {indexStatus.chunk_count} chunks</p>
            ) : (
              <p>No index found</p>
            )}
          </div>
        )}
      </div>
    </aside>
  );
}
