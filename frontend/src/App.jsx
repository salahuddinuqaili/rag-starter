import { useCallback, useEffect, useState } from "react";
import { fetchHealth, fetchIndexStatus } from "./api";
import ChatView from "./components/ChatView";
import HealthCheck from "./components/HealthCheck";
import IndexForm from "./components/IndexForm";
import Settings from "./components/Settings";

const DEFAULT_SETTINGS = {
  chunkSize: 500,
  chunkOverlap: 50,
  topK: 5,
  model: "llama3.1:8b",
  embedModel: "nomic-embed-text",
  dbPath: "./chroma_db",
};

function hasModel(health, modelName) {
  if (!health?.models) return false;
  return Object.keys(health.models).some((m) => m.startsWith(modelName));
}

export default function App() {
  const [health, setHealth] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [messages, setMessages] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const allChecksPass =
    health?.ollama &&
    hasModel(health, settings.model) &&
    hasModel(health, settings.embedModel);

  const refreshStatus = useCallback(async () => {
    try {
      const [h, s] = await Promise.all([
        fetchHealth(),
        fetchIndexStatus(settings.dbPath),
      ]);
      setHealth(h);
      setIndexStatus(s);
    } catch {
      setHealth({ ollama: false, models: {} });
      setIndexStatus({ indexed: false, chunk_count: 0 });
    }
  }, [settings.dbPath]);

  useEffect(() => {
    refreshStatus();
  }, [refreshStatus]);

  const onIndexed = useCallback(
    (stats) => {
      setIndexStatus({ indexed: true, chunk_count: stats.chunks_created });
    },
    [],
  );

  const step = !allChecksPass ? "setup" : !indexStatus?.indexed ? "index" : "chat";

  return (
    <div className="min-h-screen flex flex-col">
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shrink-0">
        <h1 className="text-lg font-semibold tracking-tight">rag-starter</h1>
        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="text-sm px-3 py-1.5 rounded-md border border-gray-300 hover:bg-gray-50"
        >
          Settings
        </button>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto px-6 py-8 space-y-6">
            <HealthCheck health={health} settings={settings} onRefresh={refreshStatus} />

            {allChecksPass && (
              <IndexForm
                settings={settings}
                indexStatus={indexStatus}
                onIndexed={onIndexed}
              />
            )}

            {allChecksPass && indexStatus?.indexed && (
              <ChatView
                settings={settings}
                messages={messages}
                setMessages={setMessages}
              />
            )}

            {step === "chat" && messages.length === 0 && (
              <p className="text-center text-gray-400 text-sm pt-4">
                Everything is set up. Ask your first question below.
              </p>
            )}
          </div>
        </main>

        {sidebarOpen && (
          <Settings
            settings={settings}
            setSettings={setSettings}
            indexStatus={indexStatus}
            onClose={() => setSidebarOpen(false)}
          />
        )}
      </div>
    </div>
  );
}
