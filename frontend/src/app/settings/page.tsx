"use client";

import { useState } from "react";
import { Settings, ShieldCheck, Users, Key, Save } from "lucide-react";

export default function SettingsPage() {
  const [orgName, setOrgName] = useState("Acme Security Corp");
  const [criticalThreshold, setCriticalThreshold] = useState(70);
  const [highThreshold, setHighThreshold] = useState(40);
  const [apiKey, setApiKey] = useState("ps_live_9f8a3c71d02e485b");
  const [saved, setSaved] = useState(false);

  const users = [
    { name: "Alice Admin", email: "admin@acme.com", role: "Admin" },
    { name: "Bob Security", email: "bob@acme.com", role: "Security Engineer" },
    { name: "Charlie Viewer", email: "charlie@acme.com", role: "Viewer" },
  ];

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div style={{ maxWidth: 1000, margin: "30px auto 0", padding: "0 24px" }}>
      <div style={{ marginBottom: 24 }}>
        <h1 style={{ fontSize: "2rem", fontWeight: 800, color: "#f8fafc" }}>Organization & RBAC Settings</h1>
        <p style={{ color: "var(--text-muted)", fontSize: "0.9rem", marginTop: 4 }}>
          Manage security risk score thresholds, role-based access control (RBAC), and API keys.
        </p>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
        {/* Org Details & Thresholds */}
        <div className="card">
          <h2 style={{ fontSize: "1.2rem", fontWeight: 700, color: "#f8fafc", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Settings size={20} color="var(--accent-cyan)" /> Organization Profile & Risk Thresholds
          </h2>

          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 20 }}>
            <div>
              <label style={{ fontSize: "0.85rem", color: "var(--text-muted)", display: "block", marginBottom: 6 }}>
                Organization Name
              </label>
              <input
                type="text"
                className="input-field"
                value={orgName}
                onChange={(e) => setOrgName(e.target.value)}
              />
            </div>
            <div>
              <label style={{ fontSize: "0.85rem", color: "var(--text-muted)", display: "block", marginBottom: 6 }}>
                Critical Severity Risk Threshold (0-100)
              </label>
              <input
                type="number"
                className="input-field"
                value={criticalThreshold}
                onChange={(e) => setCriticalThreshold(Number(e.target.value))}
              />
            </div>
          </div>

          <div style={{ display: "flex", justifyContent: "flex-end" }}>
            <button className="btn-primary" onClick={handleSave}>
              <Save size={16} /> {saved ? "Saved Settings!" : "Save Configuration"}
            </button>
          </div>
        </div>

        {/* RBAC Role Management */}
        <div className="card">
          <h2 style={{ fontSize: "1.2rem", fontWeight: 700, color: "#f8fafc", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Users size={20} color="var(--accent-emerald)" /> Role-Based Access Control (RBAC)
          </h2>

          <table style={{ width: "100%", borderCollapse: "collapse", textAlign: "left" }}>
            <thead>
              <tr style={{ borderBottom: "1px solid var(--border-color)", color: "var(--text-muted)", fontSize: "0.8rem" }}>
                <th style={{ padding: "10px 0" }}>User</th>
                <th style={{ padding: "10px 0" }}>Email</th>
                <th style={{ padding: "10px 0" }}>Assigned Role</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u, i) => (
                <tr key={i} style={{ borderBottom: "1px solid var(--border-color)" }}>
                  <td style={{ padding: "12px 0", fontWeight: 600, color: "#f8fafc" }}>{u.name}</td>
                  <td style={{ padding: "12px 0", color: "var(--text-muted)", fontSize: "0.85rem" }}>{u.email}</td>
                  <td style={{ padding: "12px 0" }}>
                    <span className="badge badge-LOW">{u.role}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* REST API Key */}
        <div className="card">
          <h2 style={{ fontSize: "1.2rem", fontWeight: 700, color: "#f8fafc", marginBottom: 16, display: "flex", alignItems: "center", gap: 8 }}>
            <Key size={20} color="var(--accent-amber)" /> API Tokens for CI & GitHub Actions
          </h2>
          <div style={{ background: "#070a12", border: "1px solid var(--border-color)", padding: 16, borderRadius: 8, fontFamily: "var(--font-mono)", fontSize: "0.9rem", color: "var(--accent-cyan)", display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <span>{apiKey}</span>
            <span style={{ fontSize: "0.75rem", color: "var(--text-dim)", textTransform: "uppercase" }}>Active Token</span>
          </div>
        </div>
      </div>
    </div>
  );
}
