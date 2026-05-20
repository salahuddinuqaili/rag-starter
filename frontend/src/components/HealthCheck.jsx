const CHECK_ITEMS = [
  { key: "ollama", label: "Ollama is running", fix: "Start it with: ollama serve" },
  {
    key: "llama3.1:8b",
    label: "LLM model (llama3.1:8b)",
    fix: "Pull it with: ollama pull llama3.1:8b",
    isModel: true,
  },
  {
    key: "nomic-embed-text",
    label: "Embedding model (nomic-embed-text)",
    fix: "Pull it with: ollama pull nomic-embed-text",
    isModel: true,
  },
];

function getStatus(health, item) {
  if (!health) return null;
  if (item.isModel) return health.models?.[item.key] ?? false;
  return health[item.key] ?? false;
}

export default function HealthCheck({ health, onRefresh }) {
  const allPass = health?.ollama
    && health?.models?.["llama3.1:8b"]
    && health?.models?.["nomic-embed-text"];

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-5">
      <div className="flex items-center justify-between mb-3">
        <h2 className="font-semibold text-base">
          {allPass ? "Prerequisites" : "Step 1: Check prerequisites"}
        </h2>
        <button
          onClick={onRefresh}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          Refresh
        </button>
      </div>

      <ul className="space-y-2">
        {CHECK_ITEMS.map((item) => {
          const status = getStatus(health, item);
          const loading = status === null;
          return (
            <li key={item.key} className="flex items-start gap-2 text-sm">
              <span className="mt-0.5 shrink-0">
                {loading ? (
                  <span className="text-gray-400">...</span>
                ) : status ? (
                  <span className="text-green-600">&#10003;</span>
                ) : (
                  <span className="text-red-500">&#10007;</span>
                )}
              </span>
              <div>
                <span className={status === false ? "text-red-700" : ""}>{item.label}</span>
                {status === false && (
                  <p className="text-gray-500 mt-0.5">
                    <code className="bg-gray-100 px-1.5 py-0.5 rounded text-xs">{item.fix}</code>
                  </p>
                )}
              </div>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
