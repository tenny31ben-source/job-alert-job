# ============================================================
#  JOB ALERT BOT — CONFIG
#  Edit this file to customize your search
# ============================================================

TELEGRAM_BOT_TOKEN = "8702836830:AAHCxk6YUuC0AjYFdEfMaOVXiRsvYJYhips"
TELEGRAM_CHAT_ID   = "6197077931"

# --- Job Roles to Search ---
JOB_TITLES = [
    "Business Development Executive",
    "Operations Executive",
    "Admin Executive",
    "Customer Support",
    "Operations Manager",
    "BizDev Executive",
    "Administrative Assistant",
    "Customer Service Executive",
    "Python Developer",
]

# --- Locations ---
LOCATIONS = ["Singapore", "Philippines", "India", "Remote"]

# --- Resume Keywords (used to score job relevance) ---
RESUME_KEYWORDS = [
    "business development", "operations", "admin", "customer support",
    "customer service", "python", "excel", "KPI", "retention",
    "gaming", "platform", "CRM", "reporting", "data analysis",
    "automation", "telegram", "AI", "cross-functional",
    "payment", "risk", "onboarding", "team management",
]

# --- Minimum keyword match score to send alert (out of 10) ---
MIN_SCORE = 1  # Send if at least 1 keyword matches

# --- How many jobs to fetch per search ---
MAX_JOBS_PER_SEARCH = 10
