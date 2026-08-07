"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchReportById, ScanReport } from "@/lib/api";
import RiskGauge from "@/components/RiskGauge";
import DiffViewer from "@/components/DiffViewer";
import { Download, ArrowLeft, ShieldAlert, CheckCircle, FileCode, Cpu, Copy, Check } from "lucide-react";

export default function ReportDetailPage() {
  const params = useParams();
  const scanId = params.id as string;
  const [report, setReport] = useState<ScanReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchReportById(scanId);
        setReport(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [scanId]);

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: "100px 20px", color: "var(--text-muted)" }}>
        <ShieldAlert size={40} className="animate-spin" style={{ marginBottom: 12, color: "var(--accent-cyan)" }} />
        <p>Loading security scan report analysis...</p>
      </div>
    );
  }

  if (!report) {
    return (
      <div style={{ maxWidth: 800, margin: "60px auto", textAlign: "center" }}>
        <h2>Report Not Found</h2>
        <Link href="/scan" className="btn-secondary" style={{ marginTop: 16 }}>
          Return to Scanner
        </Link>
      </div>
    );
  }

  const handleCopySafePrompt = () => {
    navigator.clipboard.writeText(report.rewrites?.safe_content || "");
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

  return (
    <div style={{ maxWidth: 1100, margin: "30px auto 0", padding: "0 24px" }}>
      {/* Navigation Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 24 }}>
        <Link href="/history" className="btn-secondary">
          <ArrowLeft size={16} /> Back to History
        </Link>

        {/* Export Dropdown / Actions */}
        <div style={{ display: "flex", gap: 10 }}>
          <a
            href={`${API_BASE}/export/${report.id}?format=pdf`}
            target="_blank"
            download
            className="btn-secondary"
          >
            <Download size={16} /> Export PDF
          </a>
          <a
            href={`${API_BASE}/export/${report.id}?format=html`}
            target="_blank"
            download
            className="btn-secondary"
          >
            Export HTML
          </a>
          <a
            href={`${API_BASE}/export/${report.id}?format=json`}
            target="_blank"
            download
            className="btn-secondary"
          >
            Export JSON
          </a>
        </div>
      </div>

      {/* Top Overview Card */}
      <div className="card" style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 24, marginBottom: 24 }}>
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 8 }}>
            <span className={`badge badge-${report.severity}`}>{report.severity}</span>
            <span style={{ fontSize: "0.8rem", color: "var(--text-dim)", fontFamily: "var(--font-mono)" }}>
              ID: {report.id}
            </span>
          </div>
          <h1 style={{ fontSize: "1.8rem", fontWeight: 800, color: "#f8fafc" }}>{report.title}</h1>
          <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: 4 }}>
            Input Type: <strong style={{ color: "#e2e8f0" }}>{report.input_type}</strong> | Findings:{" "}
            <strong style={{ color: "var(--accent-cyan)" }}>{report.findings.length}</strong>
          </p>
        </div>

        <RiskGauge score={report.risk_score} severity={report.severity} />
      </div>

      {/* Metrics Row */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 16, marginBottom: 24 }}>
        <div className="card" style={{ padding: 16, textAlign: "center" }}>
          <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", textTransform: "uppercase" }}>Critical Risks</div>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--accent-rose)", marginTop: 4 }}>
            {report.metrics?.critical_count ?? report.findings.filter(f => f.severity === "CRITICAL").length}
          </div>
        </div>
        <div className="card" style={{ padding: 16, textAlign: "center" }}>
          <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", textTransform: "uppercase" }}>High Vulnerabilities</div>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--accent-amber)", marginTop: 4 }}>
            {report.metrics?.high_count ?? report.findings.filter(f => f.severity === "HIGH").length}
          </div>
        </div>
        <div className="card" style={{ padding: 16, textAlign: "center" }}>
          <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", textTransform: "uppercase" }}>Lines Evaluated</div>
          <div style={{ fontSize: "1.6rem", fontWeight: 800, color: "var(--accent-cyan)", marginTop: 4 }}>
            {report.metrics?.total_lines ?? 1}
          </div>
        </div>
        <div className="card" style={{ padding: 16, textAlign: "center" }}>
          <div style={{ fontSize: "0.75rem", color: "var(--text-dim)", textTransform: "uppercase" }}>Scan Status</div>
          <div style={{ fontSize: "1.2rem", fontWeight: 700, color: "var(--accent-emerald)", marginTop: 8, textTransform: "uppercase" }}>
            {report.status}
          </div>
        </div>
      </div>

      {/* Findings Breakdown */}
      <div className="card" style={{ marginBottom: 32 }}>
        <h2 style={{ fontSize: "1.25rem", fontWeight: 700, color: "#f8fafc", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
          <ShieldAlert size={20} color="var(--accent-rose)" />
          Vulnerability Findings & Evidence ({report.findings.length})
        </h2>

        {report.findings.length === 0 ? (
          <div style={{ padding: "30px", textAlign: "center", color: "var(--accent-emerald)" }}>
            <CheckCircle size={36} style={{ marginBottom: 8 }} />
            <p style={{ fontWeight: 600 }}>No Security Vulnerabilities Detected!</p>
            <p style={{ fontSize: "0.85rem", color: "var(--text-muted)" }}>This prompt passed all signature rules, secret regexes, and obfuscation checks.</p>
          </div>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {report.findings.map((f, idx) => (
              <div
                key={idx}
                style={{
                  background: "#070a12",
                  borderLeft: `4px solid ${f.severity === 'CRITICAL' ? 'var(--accent-rose)' : f.severity === 'HIGH' ? 'var(--accent-amber)' : 'var(--accent-cyan)'}`,
                  border: "1px solid var(--border-color)",
                  borderRadius: 8,
                  padding: 16,
                }}
              >
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
                  <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                    <span className={`badge badge-${f.severity}`}>{f.severity}</span>
                    <span style={{ fontWeight: 700, color: "#f8fafc" }}>
                      {f.rule_id} - {f.rule_name}
                    </span>
                  </div>
                  <span style={{ fontSize: "0.8rem", color: "var(--text-dim)", fontFamily: "var(--font-mono)" }}>
                    Category: {f.category} | Line {f.line_number}
                  </span>
                </div>

                <div style={{ background: "#0d111a", padding: "10px 14px", borderRadius: 6, margin: "10px 0", fontFamily: "var(--font-mono)", fontSize: "0.85rem", color: "#fda4af" }}>
                  <strong>Evidence Snippet:</strong> {f.evidence}
                </div>

                <p style={{ fontSize: "0.85rem", color: "var(--text-muted)", lineHeight: 1.5 }}>
                  <strong style={{ color: "#e2e8f0" }}>Remediation Guidance:</strong> {f.remediation}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Safe Prompt Rewrite Diff Section */}
      <div className="card">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <h2 style={{ fontSize: "1.25rem", fontWeight: 700, color: "#f8fafc", display: "flex", alignItems: "center", gap: 8 }}>
            <FileCode size={20} color="var(--accent-cyan)" />
            Safe Prompt Rewrite & Diff View
          </h2>
          <button className="btn-secondary" onClick={handleCopySafePrompt}>
            {copied ? <Check size={16} color="var(--accent-emerald)" /> : <Copy size={16} />}
            {copied ? "Copied Safe Prompt" : "Copy Safe Prompt"}
          </button>
        </div>

        <DiffViewer
          lineDiffs={report.rewrites?.line_diffs || []}
          safeContent={report.rewrites?.safe_content || ""}
        />
      </div>
    </div>
  );
}
