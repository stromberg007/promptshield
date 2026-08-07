"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ShieldAlert, Scan, History, Settings, FileSpreadsheet } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();

  const navItems = [
    { label: "Scanner", href: "/scan", icon: Scan },
    { label: "Scan History", href: "/history", icon: History },
    { label: "Org Settings", href: "/settings", icon: Settings },
  ];

  return (
    <header style={{ borderBottom: "1px solid var(--border-color)", background: "rgba(11, 15, 25, 0.9)", backdropFilter: "blur(8px)", position: "sticky", top: 0, zIndex: 50 }}>
      <div style={{ maxWidth: 1280, margin: "0 auto", padding: "0 24px", height: 64, display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <Link href="/scan" style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ background: "linear-gradient(135deg, #06b6d4, #3b82f6)", width: 36, height: 36, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", color: "white" }}>
            <ShieldAlert size={22} />
          </div>
          <div>
            <span style={{ fontWeight: 800, fontSize: "1.2rem", letterSpacing: "-0.02em", color: "#f8fafc" }}>
              Prompt<span style={{ color: "var(--accent-cyan)" }}>Shield</span> AI
            </span>
            <span style={{ fontSize: "0.65rem", background: "rgba(6,182,212,0.15)", color: "#38bdf8", border: "1px solid rgba(6,182,212,0.3)", borderRadius: 4, padding: "1px 6px", marginLeft: 8, textTransform: "uppercase", fontWeight: 700 }}>
              Static Scanner v1.0
            </span>
          </div>
        </Link>

        <nav style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || (item.href === "/scan" && pathname === "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  padding: "8px 14px",
                  borderRadius: 8,
                  fontSize: "0.9rem",
                  fontWeight: 500,
                  color: isActive ? "white" : "var(--text-muted)",
                  background: isActive ? "var(--bg-elevated)" : "transparent",
                  border: isActive ? "1px solid var(--border-bright)" : "1px solid transparent",
                  transition: "all 0.2s ease",
                }}
              >
                <Icon size={16} style={{ color: isActive ? "var(--accent-cyan)" : "inherit" }} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
