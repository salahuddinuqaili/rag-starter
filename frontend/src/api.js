const BASE = "";

// --- Health & Legacy ---

export async function fetchHealth() {
  const res = await fetch(`${BASE}/api/health`);
  return res.json();
}

export async function fetchIndexStatus(dbPath = "./chroma_db") {
  const params = new URLSearchParams({ db_path: dbPath });
  const res = await fetch(`${BASE}/api/index/status?${params}`);
  return res.json();
}

// --- Collections ---

export async function fetchCollections() {
  const res = await fetch(`${BASE}/api/collections`);
  return res.json();
}

export async function createCollection(name) {
  const res = await fetch(`${BASE}/api/collections`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error((await res.json()).message || "Failed to create collection");
  return res.json();
}

export async function deleteCollection(name) {
  await fetch(`${BASE}/api/collections/${encodeURIComponent(name)}`, { method: "DELETE" });
}

export async function postCollectionIndex(name, { folderPath, chunkSize, chunkOverlap, embedModel }) {
  const res = await fetch(`${BASE}/api/collections/${encodeURIComponent(name)}/index`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      folder_path: folderPath, chunk_size: chunkSize,
      chunk_overlap: chunkOverlap, embed_model: embedModel,
    }),
  });
  if (!res.ok) throw new Error((await res.json()).message || "Indexing failed");
  return res.json();
}

export async function uploadFile(collectionName, file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/api/collections/${encodeURIComponent(collectionName)}/upload`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error((await res.json()).message || "Upload failed");
  return res.json();
}

export async function fetchDocuments(collectionName) {
  const res = await fetch(`${BASE}/api/collections/${encodeURIComponent(collectionName)}/documents`);
  return res.json();
}

export async function deleteDocument(collectionName, source) {
  await fetch(
    `${BASE}/api/collections/${encodeURIComponent(collectionName)}/documents/${encodeURIComponent(source)}`,
    { method: "DELETE" },
  );
}

// --- Conversations ---

export async function fetchConversations(collection) {
  const params = collection ? `?collection=${encodeURIComponent(collection)}` : "";
  const res = await fetch(`${BASE}/api/conversations${params}`);
  return res.json();
}

export async function createConversation(collection) {
  const res = await fetch(`${BASE}/api/conversations`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ collection }),
  });
  return res.json();
}

export async function fetchConversation(id) {
  const res = await fetch(`${BASE}/api/conversations/${id}`);
  return res.json();
}

export async function deleteConversation(id) {
  await fetch(`${BASE}/api/conversations/${id}`, { method: "DELETE" });
}

export async function addMessage(convId, { role, content, sources }) {
  const res = await fetch(`${BASE}/api/conversations/${convId}/messages`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ role, content, sources: sources || null }),
  });
  return res.json();
}

// --- SSE Streaming Query (collection-scoped) ---

export async function* streamCollectionQuery(collectionName, { question, topK, model, embedModel }) {
  const res = await fetch(`${BASE}/api/collections/${encodeURIComponent(collectionName)}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, top_k: topK, model, embed_model: embedModel }),
  });
  if (!res.ok) throw new Error((await res.json()).message || "Query failed");

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
          yield { event: currentEvent, data: JSON.parse(line.slice(6)) };
        } catch { /* skip malformed */ }
      }
    }
  }
}
