function hasModel(health, modelName) {
  if (!health?.models) return false;
  return Object.keys(health.models).some((m) => m.startsWith(modelName));
}

export default function HealthCheck({ health, settings, onRefresh }) {
  const ollamaOk = health?.ollama ?? false;
  const llmOk = ollamaOk && hasModel(health, settings.model);
  const embedOk = ollamaOk && hasModel(health, settings.embedModel);

  const items = [
    { ok: ollamaOk, label: "Ollama is running", fix: "Start it with: ollama serve" },
    {
      ok: llmOk,
      label: `LLM model (${settings.model})`,
      fix: `Pull it with: ollama pull ${settings.model}`,
    },
    {
      ok: embedOk,
      label: `Embedding model (${settings.embedModel})`,
      fix: `Pull it with: ollama pull ${settings.embedModel}`,
    },
  ];

  const allPass = ollamaOk && llmOk && embedOk;

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
        {items.map((item) => {
          const loading = health === null;
          return (
            <li key={item.label} className="flex items-start gap-2 text-sm">
              <span className="mt-0.5 shrink-0">
                {loading ? (
                  <span className="text-gray-400">...</span>
                ) : item.ok ? (
                  <span className="text-green-600">&#10003;</span>
                ) : (
                  <span className="text-red-500">&#10007;</span>
                )}
              </span>
              <div>
                <span className={!loading && !item.ok ? "text-red-700" : ""}>{item.label}</span>
                {!loading && !item.ok && (
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
