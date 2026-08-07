"use client";

interface RiskGaugeProps {
  score: number;
  severity: string;
}

export default function RiskGauge({ score, severity }: RiskGaugeProps) {
  const normalizedScore = Math.min(100, Math.max(0, score));
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (normalizedScore / 100) * circumference;

  let color = "var(--accent-emerald)";
  if (normalizedScore >= 70 || severity === "CRITICAL") color = "var(--accent-rose)";
  else if (normalizedScore >= 40 || severity === "HIGH") color = "var(--accent-amber)";
  else if (normalizedScore >= 20 || severity === "MEDIUM") color = "#fef08a";

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", position: "relative", width: 140, height: 140 }}>
      <svg width="140" height="140" viewBox="0 0 140 140">
        <circle
          cx="70"
          cy="70"
          r={radius}
          fill="transparent"
          stroke="#1e293b"
          strokeWidth="12"
        />
        <circle
          cx="70"
          cy="70"
          r={radius}
          fill="transparent"
          stroke={color}
          strokeWidth="12"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          transform="rotate(-90 70 70)"
          style={{ transition: "stroke-dashoffset 0.8s ease-out" }}
        />
      </svg>
      <div style={{ position: "absolute", textAlign: "center" }}>
        <div style={{ fontSize: "2rem", fontWeight: 800, lineHeight: 1, color: "#f8fafc" }}>
          {normalizedScore}
        </div>
        <div style={{ fontSize: "0.65rem", textTransform: "uppercase", letterSpacing: "0.05em", color: "var(--text-muted)", marginTop: 2 }}>
          Risk Score
        </div>
      </div>
    </div>
  );
}
