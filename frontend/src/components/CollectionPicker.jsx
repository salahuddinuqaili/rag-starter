import { useState } from "react";

export default function CollectionPicker({
  collections, active, onSelect, onCreate, onDelete,
}) {
  const [showNew, setShowNew] = useState(false);
  const [newName, setNewName] = useState("");

  const handleCreate = () => {
    if (!newName.trim()) return;
    onCreate(newName.trim());
    setNewName("");
    setShowNew(false);
  };

  return (
    <div className="flex items-center gap-2">
      <select
        value={active}
        onChange={(e) => onSelect(e.target.value)}
        className="border border-gray-300 rounded-md px-2 py-1.5 text-sm bg-white"
      >
        {collections.map((c) => (
          <option key={c.name} value={c.name}>{c.name}</option>
        ))}
      </select>

      {showNew ? (
        <div className="flex items-center gap-1">
          <input
            type="text"
            value={newName}
            onChange={(e) => setNewName(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleCreate()}
            placeholder="Name..."
            className="border border-gray-300 rounded-md px-2 py-1 text-sm w-32"
            autoFocus
          />
          <button onClick={handleCreate} className="text-sm text-blue-600 hover:text-blue-800">
            Add
          </button>
          <button onClick={() => setShowNew(false)} className="text-sm text-gray-400">
            &times;
          </button>
        </div>
      ) : (
        <button
          onClick={() => setShowNew(true)}
          className="text-sm text-blue-600 hover:text-blue-800"
        >
          + New
        </button>
      )}

      {active !== "documents" && (
        <button
          onClick={() => {
            if (confirm(`Delete collection "${active}"?`)) onDelete(active);
          }}
          className="text-sm text-red-500 hover:text-red-700"
        >
          Delete
        </button>
      )}
    </div>
  );
}
