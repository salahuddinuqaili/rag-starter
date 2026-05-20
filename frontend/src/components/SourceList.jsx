import { useState } from "react";

function relevanceBadge(distance) {
  const pct = ((1 - distance) * 100).toFixed(0);
  if (pct > 70) return { text: `${pct}% match`, color: "text-green-700 bg-green-50" };
  if (pct > 40) return { text: `${pct}% match`, color: "text-amber-700 bg-amber-50" };
  return { text: `${pct}% match`, color: "text-red-700 bg-red-50" };
}

export default function SourceList({ sources }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="mt-3 border-t border-gray-200 pt-2">
      <button
        onClick={() => setOpen(!open)}
        className="text-xs text-gray-500 hover:text-gray-700 flex items-center gap-1"
      >
        <span className={`transition-transform ${open ? "rotate-90" : ""}`}>&#9654;</span>
        Sources ({sources.length})
      </button>

      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((src, i) => {
            const badge = relevanceBadge(src.distance);
            const name = src.metadata?.source || "unknown";
            const preview =
              src.content.length > 200
                ? src.content.slice(0, 200) + "..."
                : src.content;

            return (
              <div
                key={i}
                className="border border-gray-200 rounded p-2 text-xs"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="font-medium text-gray-700">{name}</span>
                  <span className={`px-1.5 py-0.5 rounded text-[10px] font-medium ${badge.color}`}>
                    {badge.text}
                  </span>
                </div>
                <p className="text-gray-500 whitespace-pre-wrap">{preview}</p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
