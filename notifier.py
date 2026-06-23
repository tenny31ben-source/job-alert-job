# ============================================================
#  NOTIFIER — Sends job alerts to your Telegram
# ============================================================

import requests

def send_telegram(bot_token: str, chat_id: str, message: str) -> bool:
    """Send a message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id":    chat_id,
        "text":       message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.status_code == 200
    except Exception as e:
        print(f"[Telegram] Error: {e}")
        return False


def format_job_message(job: dict) -> str:
    """Format a job as a nice Telegram message."""
    stars = "⭐" * min(job.get("score", 1), 5)
    return (
        f"🚨 <b>New Job Alert!</b>\n\n"
        f"💼 <b>{job['title']}</b>\n"
        f"🏢 {job['company']}\n"
        f"📍 {job['location']}\n"
        f"🔗 <a href='{job['url']}'>Apply Here</a>\n"
        f"📊 Match Score: {stars} ({job.get('score', 0)} keywords)\n"
        f"🌐 Source: {job['source']}"
    )


def send_summary(bot_token: str, chat_id: str, count: int):
    """Send a summary message after all alerts."""
    if count == 0:
        msg = "✅ <b>Job Scan Complete</b>\nNo new matching jobs found this time. Will check again soon!"
    else:
        msg = f"✅ <b>Job Scan Complete</b>\nSent <b>{count}</b> new job alert(s) to you. Good luck! 🍀"

    send_telegram(bot_token, chat_id, msg)


def notify_jobs(jobs: list, bot_token: str, chat_id: str):
    """Send all job alerts to Telegram."""
    if not jobs:
        send_summary(bot_token, chat_id, 0)
        return

    # Sort by score (best match first)
    jobs_sorted = sorted(jobs, key=lambda j: j.get("score", 0), reverse=True)

    sent = 0
    for job in jobs_sorted[:20]:  # Max 20 alerts per run to avoid spam
        msg = format_job_message(job)
        success = send_telegram(bot_token, chat_id, msg)
        if success:
            sent += 1
            print(f"  ✅ Sent: {job['title']} @ {job['company']}")
        else:
            print(f"  ❌ Failed to send: {job['title']}")

    send_summary(bot_token, chat_id, sent)
