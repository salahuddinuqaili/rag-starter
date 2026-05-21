import { useRef, useState } from "react";
import { uploadFile } from "../api";

export default function FileUpload({ collectionName, onUploaded }) {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const inputRef = useRef(null);

  const handleFiles = async (files) => {
    if (!files.length) return;
    setUploading(true);
    setError(null);
    setResult(null);
    try {
      const res = await uploadFile(collectionName, files[0]);
      setResult(res);
      onUploaded(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  return (
    <div>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
          dragging ? "border-blue-500 bg-blue-50" : "border-gray-300 hover:border-gray-400"
        }`}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.md,.txt"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <p className="text-sm text-gray-500">
          {uploading ? "Uploading..." : "Drop a file here or click to upload"}
        </p>
        <p className="text-xs text-gray-400 mt-1">PDF, Markdown, or TXT</p>
      </div>

      {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
      {result && (
        <p className="mt-2 text-sm text-green-700">
          Uploaded {result.source} ({result.chunks_created} chunks)
        </p>
      )}
    </div>
  );
}
