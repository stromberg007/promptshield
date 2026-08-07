import re
import httpx
from typing import Dict, List, Tuple

ALLOWED_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml", ".py", ".ts", ".js", ".prompt"}

async def fetch_github_repo_prompts(repo_url: str) -> List[Tuple[str, str]]:
    """
    Parses GitHub repo URL (e.g. https://github.com/owner/repo),
    fetches the default branch tree via GitHub API or raw archive,
    and returns a list of tuples: (filename, file_content).
    """
    match = re.search(r"github\.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL format. Use https://github.com/owner/repo")

    owner, repo = match.group(1), match.group(2).replace(".git", "")

    # Query GitHub API tree
    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(api_url, headers={"User-Agent": "PromptShield-Scanner"})
        if resp.status_code != 200:
            # Fallback try master branch
            api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
            resp = await client.get(api_url, headers={"User-Agent": "PromptShield-Scanner"})

        if resp.status_code != 200:
            raise RuntimeError(f"Failed to fetch repository structure from GitHub API (HTTP {resp.status_code})")

        tree_data = resp.json().get("tree", [])
        
        target_files = []
        for item in tree_data:
            path = item.get("path", "")
            file_type = item.get("type", "")
            if file_type == "blob" and any(path.endswith(ext) for ext in ALLOWED_EXTENSIONS):
                target_files.append(path)

        # Limit to max 20 target prompt/config files per repo scan for responsiveness
        results = []
        for filepath in target_files[:20]:
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{filepath}"
            raw_resp = await client.get(raw_url, headers={"User-Agent": "PromptShield-Scanner"})
            if raw_resp.status_code == 200:
                results.append((filepath, raw_resp.text))

        return results
