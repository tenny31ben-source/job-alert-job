# 🤖 Job Alert Bot

Automatically scans LinkedIn, Indeed, and JobStreet every 4 hours and sends matching job alerts to your Telegram.

---

## 📁 Files

| File | Purpose |
|------|---------|
| `config.py` | Your job titles, locations, keywords |
| `scraper.py` | Scrapes job sites |
| `matcher.py` | Filters by resume keywords, removes duplicates |
| `notifier.py` | Sends Telegram messages |
| `main.py` | Entry point — run this |
| `.github/workflows/job_alert.yml` | Auto-runs every 4 hours on GitHub |

---

## 🚀 Setup (One Time)

### Step 1 — Upload to GitHub
1. Go to [github.com](https://github.com) → Create account (free)
2. Click **New Repository** → Name: `job-alert-bot` → Private → Create
3. Upload all files from this folder

### Step 2 — Enable GitHub Actions
1. Go to your repo → Click **Actions** tab
2. Click **"I understand my workflows, enable them"**

### Step 3 — Done! ✅
The bot will now run every 4 hours automatically and send you Telegram alerts.

---

## ▶️ Run Manually (on your PC)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py
```

---

## ✏️ Customize

Edit `config.py` to:
- Add/remove job titles
- Change locations
- Add more resume keywords
- Change `MIN_SCORE` (higher = stricter matching)

---

## 📱 What Telegram Alert Looks Like

```
🚨 New Job Alert!

💼 Business Development Executive
🏢 TechCorp Pte Ltd
📍 Singapore
🔗 Apply Here
📊 Match Score: ⭐⭐⭐ (3 keywords)
🌐 Source: LinkedIn
```

---

## ⚠️ Important

- **Revoke and regenerate your Telegram Bot Token** via @BotFather after uploading to GitHub (never share tokens publicly)
- Add your token as a **GitHub Secret** for production use:
  - Repo → Settings → Secrets → New secret → `TELEGRAM_BOT_TOKEN`
  - Then in `config.py` use: `os.environ.get("TELEGRAM_BOT_TOKEN")`
