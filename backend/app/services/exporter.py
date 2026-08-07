import json
from datetime import datetime
from jinja2 import Template
from fpdf import FPDF

HTML_REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PromptShield AI Security Report - {{ scan.title }}</title>
  <style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 40px; }
    .card { background-color: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 24px; margin-bottom: 24px; }
    h1, h2, h3 { color: #f0f6fc; }
    .badge { display: inline-block; padding: 4px 12px; border-radius: 12px; font-weight: bold; font-size: 14px; text-transform: uppercase; }
    .badge-CRITICAL { background-color: #7d1a1a; color: #ff7b72; border: 1px solid #f85149; }
    .badge-HIGH { background-color: #5a3000; color: #ffa657; border: 1px solid #d29922; }
    .badge-MEDIUM { background-color: #3b3000; color: #e3b341; border: 1px solid #bb8009; }
    .badge-PASS { background-color: #11381e; color: #56d364; border: 1px solid #238636; }
    .finding { border-left: 4px solid #f85149; background-color: #21262d; padding: 12px 16px; margin-bottom: 12px; border-radius: 0 4px 4px 0; }
    code { font-family: monospace; background-color: #0d1117; padding: 2px 6px; border-radius: 4px; color: #79c0ff; }
    table { width: 100%; border-collapse: collapse; margin-top: 12px; }
    th, td { text-align: left; padding: 8px; border-bottom: 1px solid #30363d; }
  </style>
</head>
<body>
  <div class="card">
    <h1>PromptShield AI Security Report</h1>
    <p><strong>Scan Title:</strong> {{ scan.title }}</p>
    <p><strong>Input Type:</strong> {{ scan.input_type }} | <strong>Scan ID:</strong> {{ scan.id }}</p>
    <p><strong>Overall Risk Score:</strong> <span style="font-size: 24px; font-weight: bold;">{{ scan.risk_score }}/100</span></p>
    <p><strong>Severity:</strong> <span class="badge badge-{{ scan.severity }}">{{ scan.severity }}</span></p>
  </div>

  <div class="card">
    <h2>Vulnerability Findings ({{ scan.findings_json|length }})</h2>
    {% if scan.findings_json %}
      {% for f in scan.findings_json %}
        <div class="finding">
          <h3>[{{ f.severity }}] {{ f.rule_id }} - {{ f.rule_name }}</h3>
          <p><strong>Category:</strong> {{ f.category }} | <strong>Line:</strong> {{ f.line_number }}</p>
          <p><strong>Evidence Snippet:</strong> <code>{{ f.evidence }}</code></p>
          <p><strong>Remediation Guidance:</strong> {{ f.remediation }}</p>
        </div>
      {% endfor %}
    {% else %}
      <p style="color: #56d364;">No vulnerability signatures or injection patterns detected!</p>
    {% endif %}
  </div>

  <div class="card">
    <h2>Safe Prompt Sanitized Rewrite</h2>
    <pre style="background: #0d1117; padding: 16px; border-radius: 6px; white-space: pre-wrap; color: #a5d6ff;">{{ scan.rewrites_json.safe_content }}</pre>
  </div>
</body>
</html>
"""

def generate_json_report(scan_data: dict) -> str:
    return json.dumps(scan_data, indent=2, default=str)

def generate_html_report(scan_data: dict) -> str:
    template = Template(HTML_REPORT_TEMPLATE)
    return template.render(scan=scan_data)

def generate_pdf_report(scan_data: dict) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, "PromptShield AI - Security Report", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Target: {scan_data.get('title', 'Scan Result')}", ln=True)
    pdf.cell(0, 8, f"Risk Score: {scan_data.get('risk_score', 0)} / 100", ln=True)
    pdf.cell(0, 8, f"Severity: {scan_data.get('severity', 'PASS')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Detected Vulnerabilities ({len(scan_data.get('findings_json', []))})", ln=True)
    pdf.set_font("Helvetica", "", 10)

    for idx, f in enumerate(scan_data.get("findings_json", []), start=1):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(0, 6, f"{idx}. [{f.get('severity')}] {f.get('rule_id')} - {f.get('rule_name')}", ln=True)
        pdf.set_font("Helvetica", "", 9)
        pdf.cell(0, 5, f"   Category: {f.get('category')} | Line: {f.get('line_number')}", ln=True)
        pdf.cell(0, 5, f"   Evidence: {str(f.get('evidence'))[:80]}", ln=True)
        pdf.multi_cell(0, 5, f"   Remediation: {f.get('remediation')}")
        pdf.ln(2)

    return bytes(pdf.output())
