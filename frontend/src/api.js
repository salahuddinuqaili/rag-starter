const BASE = "";

export async function fetchHealth() {
  const res = await fetch(`${BASE}/api/health`);
  return res.json();
}

export async function fetchIndexStatus(dbPath = "./chroma_db") {
  const params = new URLSearchParams({ db_path: dbPath });
  const res = await fetch(`${BASE}/api/index/status?${params}`);
  return res.json();
}

export async function postIndex({ folderPath, chunkSize, chunkOverlap, dbPath }) {
  const res = await fetch(`${BASE}/api/index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      folder_path: folderPath,
      chunk_size: chunkSize,
      chunk_overlap: chunkOverlap,
      db_path: dbPath,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Indexing failed");
  }
  return res.json();
}

/**
 * POST-based SSE stream for /api/query.
 * Yields { event, data } objects as they arrive.
 */
export async function* streamQuery({ question, topK, model, dbPath }) {
  const res = await fetch(`${BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      top_k: topK,
      model,
      db_path: dbPath,
    }),
  });

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.message || "Query failed");
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let currentEvent = "message";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop();

    for (const line of lines) {
      if (line.startsWith("event: ")) {
        currentEvent = line.slice(7).trim();
      } else if (line.startsWith("data: ")) {
        try {
          const data = JSON.parse(line.slice(6));
          yield { event: currentEvent, data };
        } catch {
          // Skip malformed JSON lines
        }
      }
    }
  }
}
