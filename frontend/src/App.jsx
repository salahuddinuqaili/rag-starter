import { useCallback, useEffect, useState } from "react";
import {
  createCollection, deleteCollection, deleteConversation,
  fetchCollections, fetchConversation, fetchConversations,
  fetchHealth, fetchIndexStatus,
} from "./api";
import ChatView from "./components/ChatView";
import CollectionPicker from "./components/CollectionPicker";
import ConversationList from "./components/ConversationList";
import HealthCheck from "./components/HealthCheck";
import IndexForm from "./components/IndexForm";
import Settings from "./components/Settings";

const DEFAULT_SETTINGS = {
  chunkSize: 500, chunkOverlap: 50, topK: 5,
  model: "llama3.1:8b", embedModel: "nomic-embed-text", dbPath: "./chroma_db",
};

function hasModel(health, name) {
  if (!health?.models) return false;
  return Object.keys(health.models).some((m) => m.startsWith(name));
}

export default function App() {
  const [health, setHealth] = useState(null);
  const [indexStatus, setIndexStatus] = useState(null);
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Collections
  const [collections, setCollections] = useState([]);
  const [activeCollection, setActiveCollection] = useState("documents");

  // Conversations
  const [conversations, setConversations] = useState([]);
  const [activeConvId, setActiveConvId] = useState(null);
  const [messages, setMessages] = useState([]);

  const allChecksPass =
    health?.ollama && hasModel(health, settings.model) && hasModel(health, settings.embedModel);

  // --- Data fetching ---

  const refreshHealth = useCallback(async () => {
    try {
      setHealth(await fetchHealth());
    } catch {
      setHealth({ ollama: false, models: {} });
    }
  }, []);

  const refreshCollections = useCallback(async () => {
    try {
      const cols = await fetchCollections();
      setCollections(cols);
      if (cols.length > 0 && !cols.find((c) => c.name === activeCollection)) {
        setActiveCollection(cols[0].name);
      }
    } catch { /* ignore */ }
  }, [activeCollection]);

  const refreshIndex = useCallback(async () => {
    try {
      setIndexStatus(await fetchIndexStatus(settings.dbPath));
    } catch {
      setIndexStatus({ indexed: false, chunk_count: 0 });
    }
  }, [settings.dbPath]);

  const refreshConversations = useCallback(async () => {
    try {
      setConversations(await fetchConversations(activeCollection));
    } catch {
      setConversations([]);
    }
  }, [activeCollection]);

  useEffect(() => { refreshHealth(); }, [refreshHealth]);
  useEffect(() => { refreshCollections(); }, [refreshCollections]);
  useEffect(() => { refreshIndex(); }, [refreshIndex]);
  useEffect(() => { refreshConversations(); }, [refreshConversations]);

  // Reset chat when switching collection
  useEffect(() => {
    setActiveConvId(null);
    setMessages([]);
  }, [activeCollection]);

  // --- Handlers ---

  const handleSelectCollection = (name) => {
    setActiveCollection(name);
  };

  const handleCreateCollection = async (name) => {
    await createCollection(name);
    await refreshCollections();
    setActiveCollection(name);
  };

  const handleDeleteCollection = async (name) => {
    await deleteCollection(name);
    await refreshCollections();
    setActiveCollection("documents");
  };

  const handleSelectConversation = async (id) => {
    setActiveConvId(id);
    try {
      const conv = await fetchConversation(id);
      setMessages(
        conv.messages.map((m) => ({ role: m.role, content: m.content, sources: m.sources })),
      );
    } catch {
      setMessages([]);
    }
  };

  const handleNewChat = () => {
    setActiveConvId(null);
    setMessages([]);
  };

  const handleDeleteConversation = async (id) => {
    await deleteConversation(id);
    if (id === activeConvId) handleNewChat();
    await refreshConversations();
  };

  const handleConversationCreated = (conv) => {
    setConversations((prev) => [conv, ...prev]);
  };

  const handleIndexed = () => {
    refreshIndex();
    refreshCollections();
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shrink-0">
        <h1 className="text-lg font-semibold tracking-tight">rag-starter</h1>
        <div className="flex items-center gap-4">
          <CollectionPicker
            collections={collections}
            active={activeCollection}
            onSelect={handleSelectCollection}
            onCreate={handleCreateCollection}
            onDelete={handleDeleteCollection}
          />
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-sm px-3 py-1.5 rounded-md border border-gray-300 hover:bg-gray-50"
          >
            Settings
          </button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar: conversations */}
        {allChecksPass && indexStatus?.indexed && (
          <ConversationList
            conversations={conversations}
            activeId={activeConvId}
            onSelect={handleSelectConversation}
            onNew={handleNewChat}
            onDelete={handleDeleteConversation}
          />
        )}

        {/* Main content */}
        <main className="flex-1 overflow-y-auto">
          <div className="max-w-2xl mx-auto px-6 py-8 space-y-6">
            <HealthCheck
              health={health}
              settings={settings}
              onRefresh={refreshHealth}
            />

            {allChecksPass && (
              <IndexForm
                settings={settings}
                collectionName={activeCollection}
                indexStatus={indexStatus}
                onIndexed={handleIndexed}
              />
            )}

            {allChecksPass && indexStatus?.indexed && (
              <ChatView
                settings={settings}
                collectionName={activeCollection}
                messages={messages}
                setMessages={setMessages}
                conversationId={activeConvId}
                setConversationId={setActiveConvId}
                onConversationCreated={handleConversationCreated}
              />
            )}
          </div>
        </main>

        {/* Right sidebar: settings */}
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
