import SourceList from "./SourceList";

export default function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-lg px-4 py-2.5 text-sm leading-relaxed ${
          isUser
            ? "bg-blue-600 text-white"
            : "bg-gray-100 text-gray-900"
        }`}
      >
        {/* Render answer text with basic line break support */}
        <div className="whitespace-pre-wrap">{message.content}</div>

        {/* Sources (assistant only) */}
        {!isUser && message.sources?.length > 0 && (
          <SourceList sources={message.sources} />
        )}

        {/* Loading indicator for empty assistant messages */}
        {!isUser && !message.content && (
          <span className="text-gray-400">Thinking...</span>
        )}
      </div>
    </div>
  );
}
