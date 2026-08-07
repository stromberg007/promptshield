"use client";

import { LineDiff } from "@/lib/api";
import { CheckCircle, AlertTriangle } from "lucide-react";

interface DiffViewerProps {
  lineDiffs: LineDiff[];
  safeContent: string;
}

export default function DiffViewer({ lineDiffs, safeContent }: DiffViewerProps) {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: "#070a12", border: "1px solid var(--border-color)", padding: "12px 16px", borderRadius: "8px 8px 0 0" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.85rem", fontWeight: 600, color: "#94a3b8" }}>
          <AlertTriangle size={16} color="var(--accent-rose)" />
          Original Content (Raw)
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8, fontSize: "0.85rem", fontWeight: 600, color: "var(--accent-emerald)" }}>
          <CheckCircle size={16} />
          Sanitized Safe Prompt (Rewrite)
        </div>
      </div>

      <div className="diff-container" style={{ borderRadius: "0 0 8px 8px", marginTop: -16 }}>
        {/* Left Pane - Original */}
        <div className="diff-pane" style={{ borderRight: "1px solid var(--border-color)" }}>
          {lineDiffs.map((item) => (
            <div key={`orig-${item.line_number}`} className={`diff-line ${item.status === 'modified' ? 'modified' : ''}`}>
              <span className="num">{item.line_number}</span>
              <span style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{item.original}</span>
            </div>
          ))}
        </div>

        {/* Right Pane - Safe Rewrite */}
        <div className="diff-pane">
          {lineDiffs.map((item) => (
            <div key={`rewr-${item.line_number}`} className={`diff-line ${item.status === 'modified' ? 'added' : ''}`}>
              <span className="num">{item.line_number}</span>
              <span style={{ whiteSpace: "pre-wrap", wordBreak: "break-all" }}>{item.rewritten}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
