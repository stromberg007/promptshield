import asyncio
import httpx

API_BASE = "http://localhost:8000/api/v1"

async def main():
    repo_url = "https://github.com/langchain-ai/langchain"
    print(f"=== Testing Live GitHub Repo Scan: {repo_url} ===")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(f"{API_BASE}/scan/github", json={"repo_url": repo_url})
        if resp.status_code == 200:
            data = resp.json()
            print(f"[+] Scan Successful!")
            print(f"    - Title: {data['title']}")
            print(f"    - Scan ID: {data['id']}")
            print(f"    - Risk Score: {data['risk_score']} / 100")
            print(f"    - Severity: {data['severity']}")
            print(f"    - Total Findings: {len(data['findings'])}")
            print(f"    - Evaluated Files Lines: {data['metrics'].get('total_lines')}")
            
            if data['findings']:
                print("\n    - Sample Findings Detected:")
                for f in data['findings'][:3]:
                    print(f"      * [{f['severity']}] Line {f['line_number']}: {f['rule_name']} ({f['evidence']})")
        else:
            print(f"[-] Scan failed: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    asyncio.run(main())
