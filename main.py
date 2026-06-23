# ============================================================
#  JOB ALERT BOT — MAIN
#  Run this manually: python main.py
#  Or let GitHub Actions run it automatically every 4 hours
# ============================================================

from config   import (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
                      JOB_TITLES, LOCATIONS, RESUME_KEYWORDS,
                      MIN_SCORE, MAX_JOBS_PER_SEARCH)
from scraper  import fetch_all_jobs
from matcher  import filter_new_jobs, mark_jobs_seen
from notifier import notify_jobs, send_telegram

def main():
    print("=" * 50)
    print("🤖 Job Alert Bot Starting...")
    print("=" * 50)

    # 1. Send startup notification
    send_telegram(
        TELEGRAM_BOT_TOKEN,
        TELEGRAM_CHAT_ID,
        "🤖 <b>Job Alert Bot Running...</b>\nScanning LinkedIn, Indeed, JobStreet for new jobs! ⏳"
    )

    # 2. Scrape jobs
    raw_jobs = fetch_all_jobs(JOB_TITLES, LOCATIONS, MAX_JOBS_PER_SEARCH)

    # 3. Filter — only new + relevant jobs
    new_jobs = filter_new_jobs(raw_jobs, RESUME_KEYWORDS, MIN_SCORE)
    print(f"\n📋 New matching jobs found: {len(new_jobs)}")

    # 4. Send Telegram alerts
    notify_jobs(new_jobs, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)

    # 5. Mark as seen (so we don't send duplicates next run)
    mark_jobs_seen(new_jobs)

    print("\n✅ Job scan complete!")

if __name__ == "__main__":
    main()
