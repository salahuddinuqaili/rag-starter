import { useRef, useState } from "react";
import { streamQuery } from "../api";
import ChatMessage from "./ChatMessage";

const EXAMPLE_QUESTIONS = [
  "What are the best practices for async communication?",
  "How does supervised learning differ from unsupervised?",
  "What neighbourhoods should I visit in Berlin?",
];

export default function ChatView({ settings, messages, setMessages }) {
  const [input, setInput] = useState("");
  const [streaming, setStreaming] = useState(false);
  const bottomRef = useRef(null);

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const ask = async (question) => {
    if (!question.trim() || streaming) return;

    const userMsg = { role: "user", content: question };
    const assistantMsg = { role: "assistant", content: "", sources: [] };

    setMessages((prev) => [...prev, userMsg, assistantMsg]);
    setInput("");
    setStreaming(true);

    try {
      const stream = streamQuery({
        question,
        topK: settings.topK,
        model: settings.model,
        dbPath: settings.dbPath,
      });

      for await (const { event, data } of stream) {
        if (event === "token") {
          setMessages((prev) => {
            const updated = [...prev];
            const last = updated[updated.length - 1];
            updated[updated.length - 1] = { ...last, content: last.content + data.text };
            return updated;
          });
          scrollToBottom();
        } else if (event === "sources") {
          setMessages((prev) => {
            const updated = [...prev];
            updated[updated.length - 1] = { ...updated[updated.length - 1], sources: data };
            return updated;
          });
        }
      }
    } catch (err) {
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = {
          ...updated[updated.length - 1],
          content: `Error: ${err.message}`,
        };
        return updated;
      });
    } finally {
      setStreaming(false);
      scrollToBottom();
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    ask(input);
  };

  return (
    <section className="rounded-lg border border-gray-200 bg-white p-5">
      <h2 className="font-semibold text-base mb-3">Ask questions</h2>

      {/* Example question chips — shown when no messages yet */}
      {messages.length === 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {EXAMPLE_QUESTIONS.map((q) => (
            <button
              key={q}
              onClick={() => ask(q)}
              className="text-sm px-3 py-1.5 rounded-full border border-gray-300 hover:bg-gray-50 text-gray-700"
            >
              {q}
            </button>
          ))}
        </div>
      )}

      {/* Messages */}
      <div className="space-y-4 mb-4 max-h-[60vh] overflow-y-auto">
        {messages.map((msg, i) => (
          <ChatMessage key={i} message={msg} />
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question about your documents..."
          disabled={streaming}
          className="flex-1 border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={streaming || !input.trim()}
          className="px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {streaming ? "..." : "Ask"}
        </button>
      </form>
    </section>
  );
}
