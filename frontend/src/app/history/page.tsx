"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchScanHistory, ScanReport } from "@/lib/api";
import { Search, Filter, ShieldAlert, ArrowRight, RefreshCw } from "lucide-react";

export default function HistoryPage() {
  const [scans, setScans] = useState<ScanReport[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);

  const [severityFilter, setSeverityFilter] = useState<string>("");
  const [inputTypeFilter, setInputTypeFilter] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const loadHistory = async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (severityFilter) params.severity = severityFilter;
      if (inputTypeFilter) params.input_type = inputTypeFilter;
      if (searchQuery) params.search = searchQuery;

      const res = await fetchScanHistory(params);
      setScans(res.items);
      setTotal(res.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [severityFilter, inputTypeFilter]);

  return (
    <div style={{ maxWidth: 1200, margin: "30px auto 0", padding: "0 24px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <div>
          <h1 style={{ fontSize: "2rem", fontWeight: 800, color: "#f8fafc" }}>Scan History & Audit Logs</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: 4 }}>
            Review historical prompt security scans, threat scores, and export compliance reports.
          </p>
        </div>
        <button className="btn-secondary" onClick={loadHistory}>
          <RefreshCw size={16} className={loading ? "animate-spin" : ""} /> Refresh Logs
        </button>
      </div>

      {/* Filter Bar */}
      <div className="card" style={{ marginBottom: 24, padding: 16, display: "flex", gap: 16, alignItems: "center", flexWrap: "wrap" }}>
        <div style={{ flex: 1, minWidth: 240, display: "flex", alignItems: "center", gap: 8, background: "#070a12", border: "1px solid var(--border-color)", borderRadius: 8, padding: "8px 12px" }}>
          <Search size={16} color="var(--text-dim)" />
          <input
            type="text"
            placeholder="Search scan title..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && loadHistory()}
            style={{ background: "transparent", border: "none", color: "var(--text-main)", outline: "none", width: "100%", fontSize: "0.9rem" }}
          />
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Filter size={16} color="var(--text-dim)" />
          <select
            className="input-field"
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={{ width: 160 }}
          >
            <option value="">All Severities</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="HIGH">HIGH</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="LOW">LOW</option>
            <option value="PASS">PASS</option>
          </select>

          <select
            className="input-field"
            value={inputTypeFilter}
            onChange={(e) => setInputTypeFilter(e.target.value)}
            style={{ width: 160 }}
          >
            <option value="">All Input Types</option>
            <option value="text">Text Paste</option>
            <option value="file">File Upload</option>
            <option value="github_repo">GitHub Repo</option>
          </select>
        </div>
      </div>

      {/* History Data Table */}
      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
          <thead>
            <tr style={{ background: "#070a12", borderBottom: "1px solid var(--border-color)", color: "var(--text-muted)", fontSize: "0.8rem", textTransform: "uppercase" }}>
              <th style={{ padding: "14px 20px" }}>Scan Target</th>
              <th style={{ padding: "14px 20px" }}>Type</th>
              <th style={{ padding: "14px 20px" }}>Risk Score</th>
              <th style={{ padding: "14px 20px" }}>Severity</th>
              <th style={{ padding: "14px 20px" }}>Date</th>
              <th style={{ padding: "14px 20px", textAlign: "right" }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {loading ? (
              <tr>
                <td colSpan={6} style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
                  Loading scan history...
                </td>
              </tr>
            ) : scans.length === 0 ? (
              <tr>
                <td colSpan={6} style={{ padding: 40, textAlign: "center", color: "var(--text-muted)" }}>
                  No scans found matching filters.
                </td>
              </tr>
            ) : (
              scans.map((s) => (
                <tr key={s.id} style={{ borderBottom: "1px solid var(--border-color)" }}>
                  <td style={{ padding: "16px 20px", fontWeight: 600, color: "#f8fafc" }}>
                    {s.title}
                  </td>
                  <td style={{ padding: "16px 20px", color: "var(--text-muted)", fontSize: "0.85rem", textTransform: "capitalize" }}>
                    {s.input_type}
                  </td>
                  <td style={{ padding: "16px 20px", fontWeight: 700, fontSize: "1rem" }}>
                    <span style={{ color: s.risk_score >= 70 ? "var(--accent-rose)" : s.risk_score >= 40 ? "var(--accent-amber)" : "var(--accent-emerald)" }}>
                      {s.risk_score} / 100
                    </span>
                  </td>
                  <td style={{ padding: "16px 20px" }}>
                    <span className={`badge badge-${s.severity}`}>{s.severity}</span>
                  </td>
                  <td style={{ padding: "16px 20px", color: "var(--text-dim)", fontSize: "0.85rem" }}>
                    {s.created_at ? new Date(s.created_at).toLocaleString() : "Recently"}
                  </td>
                  <td style={{ padding: "16px 20px", textAlign: "right" }}>
                    <Link href={`/report/${s.id}`} className="btn-secondary" style={{ padding: "6px 12px", fontSize: "0.8rem" }}>
                      View Report <ArrowRight size={14} />
                    </Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
