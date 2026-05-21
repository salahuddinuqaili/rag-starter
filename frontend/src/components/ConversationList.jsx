export default function ConversationList({
  conversations, activeId, onSelect, onNew, onDelete,
}) {
  return (
    <aside className="w-56 border-r border-gray-200 bg-white flex flex-col shrink-0 overflow-hidden">
      <div className="p-3 border-b border-gray-200 flex items-center justify-between">
        <span className="text-xs font-semibold text-gray-500 uppercase tracking-wide">Chats</span>
        <button
          onClick={onNew}
          className="text-xs text-blue-600 hover:text-blue-800"
        >
          + New
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {conversations.length === 0 && (
          <p className="p-3 text-xs text-gray-400">No conversations yet</p>
        )}
        {conversations.map((c) => (
          <div
            key={c.id}
            onClick={() => onSelect(c.id)}
            className={`group flex items-center justify-between px-3 py-2 cursor-pointer text-sm border-b border-gray-100 ${
              c.id === activeId ? "bg-blue-50 text-blue-700" : "hover:bg-gray-50 text-gray-700"
            }`}
          >
            <span className="truncate flex-1">
              {c.title || "New chat"}
            </span>
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(c.id);
              }}
              className="text-gray-300 group-hover:text-red-400 hover:text-red-600 ml-2 shrink-0"
              title="Delete"
            >
              &times;
            </button>
          </div>
        ))}
      </div>
    </aside>
  );
}
