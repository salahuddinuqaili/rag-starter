import { useCallback, useEffect, useRef, useState } from "react";
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
  dbPath: "./chroma_db",
};

export default function App() {
  const [health, setHealth] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [messages, setMessages] = useState([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const healthyRef = useRef(false);

  const allChecksPass =
    health?.ollama &&
    health?.models?.["llama3.1:8b"] &&
    health?.models?.["nomic-embed-text"];

  const refreshStatus = useCallback(async () => {
    try {
      const [h, s] = await Promise.all([
        fetchHealth(),
        fetchIndexStatus(settings.dbPath),
      ]);
      setHealth(h);
      setIndexStatus(s);
      healthyRef.current =
        h.ollama && h.models["llama3.1:8b"] && h.models["nomic-embed-text"];
    } catch {
      setHealth({ ollama: false, models: { "llama3.1:8b": false, "nomic-embed-text": false } });
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

  // Determine which step to highlight
  const step = !allChecksPass ? "setup" : !indexStatus?.indexed ? "index" : "chat";

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
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
        {/* Main content */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto px-6 py-8 space-y-6">
            {/* Step 1: Health checks */}
            <HealthCheck health={health} onRefresh={refreshStatus} />

            {/* Step 2: Index (visible once checks pass) */}
            {allChecksPass && (
              <IndexForm
                settings={settings}
                indexStatus={indexStatus}
                onIndexed={onIndexed}
              />
            )}

            {/* Step 3: Chat (visible once indexed) */}
            {allChecksPass && indexStatus?.indexed && (
              <ChatView
                settings={settings}
                messages={messages}
                setMessages={setMessages}
              />
            )}

            {/* Collapsed state indicator when everything is ready */}
            {step === "chat" && messages.length === 0 && (
              <p className="text-center text-gray-400 text-sm pt-4">
                Everything is set up. Ask your first question below.
              </p>
            )}
          </div>
        </main>

        {/* Sidebar */}
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
