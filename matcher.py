# ============================================================
#  MATCHER — Scores jobs against your resume keywords
# ============================================================

import json
import os
import hashlib

SEEN_FILE = "seen_jobs.json"


def load_seen_jobs() -> set:
    """Load already-notified job IDs."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen_jobs(seen: set):
    """Save notified job IDs to file."""
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def job_id(job: dict) -> str:
    """Create a unique ID for each job to avoid duplicate alerts."""
    key = f"{job['title']}|{job['company']}|{job['location']}"
    return hashlib.md5(key.encode()).hexdigest()


def score_job(job: dict, keywords: list) -> int:
    """Score job relevance based on keyword matches in title + company."""
    text = f"{job['title']} {job['company']} {job.get('description', '')}".lower()
    return sum(1 for kw in keywords if kw.lower() in text)


def filter_new_jobs(jobs: list, keywords: list, min_score: int) -> list[dict]:
    """Return only new, relevant jobs not seen before."""
    seen = load_seen_jobs()
    new_jobs = []

    for job in jobs:
        jid = job_id(job)
        if jid in seen:
            continue  # Already sent this one

        score = score_job(job, keywords)
        if score >= min_score:
            job["score"] = score
            job["id"] = jid
            new_jobs.append(job)

    # Deduplicate within this batch
    unique = {j["id"]: j for j in new_jobs}
    return list(unique.values())


def mark_jobs_seen(jobs: list):
    """Mark jobs as seen so we don't alert twice."""
    seen = load_seen_jobs()
    for job in jobs:
        seen.add(job["id"])
    save_seen_jobs(seen)
