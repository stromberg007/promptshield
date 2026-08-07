import asyncio
from celery import Celery
from app.core.config import settings

celery_app = Celery("promptshield_tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)
celery_app.conf.task_routes = {"app.tasks.worker.*": "main-queue"}

@celery_app.task(name="scan_github_repo_async")
def scan_github_repo_async(scan_id: str, repo_url: str):
    """
    Background worker task for scanning GitHub repositories.
    Runs async detector pipeline against fetched repo prompt files.
    """
    from app.services.github_fetcher import fetch_github_repo_prompts
    from app.engine.scorer import run_full_scan
    from app.engine.diff import generate_safe_rewrite
    
    async def _run():
        try:
            files = await fetch_github_repo_prompts(repo_url)
            combined_content = ""
            for fname, content in files:
                combined_content += f"\n--- FILE: {fname} ---\n" + content

            risk_score, severity, findings, metrics = await run_full_scan(combined_content, file_name=repo_url)
            rewrites = generate_safe_rewrite(combined_content, findings)

            # In a production worker, results are persisted back to DB via AsyncSession
            return {
                "scan_id": scan_id,
                "status": "completed",
                "risk_score": risk_score,
                "severity": severity,
                "findings": findings,
                "rewrites": rewrites,
                "metrics": metrics
            }
        except Exception as e:
            return {"scan_id": scan_id, "status": "failed", "error": str(e)}

    return asyncio.run(_run())
