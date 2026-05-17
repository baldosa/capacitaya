import React, { useState } from "react";
import { AppLayout } from "@/components/AppLayout";
import { Play, Loader2 } from "lucide-react";

interface Endpoint {
  label: string;
  path: string;
  param?: { name: string; placeholder: string };
}

const ENDPOINTS: Endpoint[] = [
  { label: "GET /health", path: "/health" },
  { label: "GET /users", path: "/api/users" },
  { label: "GET /learning-paths", path: "/api/learning-paths" },
  { label: "GET /job-descriptions", path: "/api/job-descriptions" },
  {
    label: "GET /students/{email}/learning-paths",
    path: "/api/students/{email}/learning-paths",
    param: { name: "email", placeholder: "estudiante@ejemplo.com" },
  },
  {
    label: "GET /students/{email}/attempts",
    path: "/api/students/{email}/attempts",
    param: { name: "email", placeholder: "estudiante@ejemplo.com" },
  },
];

export function DemoApi() {
  const [selected, setSelected] = useState<Endpoint>(ENDPOINTS[0]);
  const [param, setParam] = useState("");
  const [result, setResult] = useState<unknown>(null);
  const [status, setStatus] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const resolvedPath = selected.param
    ? selected.path.replace(`{${selected.param.name}}`, encodeURIComponent(param))
    : selected.path;

  async function run() {
    setLoading(true);
    setError(null);
    setResult(null);
    setStatus(null);
    try {
      const res = await fetch(resolvedPath);
      setStatus(res.status);
      const text = await res.text();
      try {
        setResult(JSON.parse(text));
      } catch {
        setResult(text);
      }
    } catch (e) {
      setError(String(e));
    } finally {
      setLoading(false);
    }
  }

  const statusColor =
    status === null ? "" : status < 300 ? "text-green-400" : "text-red-400";

  return (
    <AppLayout activePage="Demo API">
      <div className="space-y-4 max-w-3xl">
        <div className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 space-y-4">
          <h2 className="font-bold text-lg">Demo de endpoints</h2>

          {/* Selector */}
          <div className="flex flex-col sm:flex-row gap-3">
            <select
              className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
              value={selected.path}
              onChange={(e) => {
                const ep = ENDPOINTS.find((ep) => ep.path === e.target.value)!;
                setSelected(ep);
                setParam("");
                setResult(null);
                setStatus(null);
                setError(null);
              }}
            >
              {ENDPOINTS.map((ep) => (
                <option key={ep.path} value={ep.path}>
                  {ep.label}
                </option>
              ))}
            </select>

            <button
              onClick={run}
              disabled={loading || (!!selected.param && !param.trim())}
              className="flex items-center gap-2 px-5 py-2.5 bg-[#4F46E5] hover:bg-indigo-700 disabled:opacity-50 text-white font-semibold rounded-xl text-sm transition-colors"
            >
              {loading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Play className="w-4 h-4" />
              )}
              Consultar
            </button>
          </div>

          {/* Param input */}
          {selected.param && (
            <input
              type="text"
              placeholder={selected.param.placeholder}
              value={param}
              onChange={(e) => setParam(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && run()}
              className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm bg-slate-50 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500"
            />
          )}

          {/* URL preview */}
          <p className="text-xs text-slate-400 font-mono">
            {window.location.origin}{resolvedPath}
          </p>
        </div>

        {/* Response */}
        {(result !== null || error) && (
          <div className="bg-slate-900 rounded-2xl overflow-hidden">
            <div className="flex items-center gap-3 px-5 py-3 border-b border-slate-700">
              <span className="text-xs text-slate-400 font-mono">{resolvedPath}</span>
              {status && (
                <span className={`text-xs font-bold font-mono ml-auto ${statusColor}`}>
                  {status}
                </span>
              )}
            </div>
            <div className="p-5 overflow-auto max-h-[60vh]">
              {error ? (
                <p className="text-red-400 text-sm font-mono">{error}</p>
              ) : (
                <pre className="text-green-400 text-sm font-mono whitespace-pre-wrap">
                  {JSON.stringify(result, null, 2)}
                </pre>
              )}
            </div>
          </div>
        )}
      </div>
    </AppLayout>
  );
}
