# ============================================================
#  SCRAPER — Fetches jobs from multiple sources
# ============================================================

import requests
from bs4 import BeautifulSoup
import urllib.parse
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def scrape_indeed(title: str, location: str, max_results: int = 10) -> list[dict]:
    """Scrape Indeed for jobs."""
    jobs = []
    query = urllib.parse.urlencode({"q": title, "l": location})
    url = f"https://www.indeed.com/jobs?{query}&sort=date"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", class_="job_seen_beacon")[:max_results]

        for card in cards:
            try:
                job_title = card.find("span", {"title": True})
                company   = card.find("span", {"data-testid": "company-name"})
                loc       = card.find("div",  {"data-testid": "text-location"})
                link_tag  = card.find("a", href=True)

                jobs.append({
                    "title":    job_title.text.strip() if job_title else title,
                    "company":  company.text.strip()   if company   else "Unknown",
                    "location": loc.text.strip()       if loc       else location,
                    "source":   "Indeed",
                    "url":      "https://www.indeed.com" + link_tag["href"] if link_tag else url,
                })
            except Exception:
                continue

    except Exception as e:
        print(f"[Indeed] Error scraping '{title}' in '{location}': {e}")

    return jobs


def scrape_jobstreet(title: str, location: str, max_results: int = 10) -> list[dict]:
    """Scrape JobStreet for jobs."""
    jobs = []
    location_map = {
        "Singapore":   "singapore",
        "Philippines": "philippines",
        "India":       "india",
        "Remote":      "singapore",  # fallback
    }
    loc_slug = location_map.get(location, "singapore")
    title_slug = urllib.parse.quote_plus(title)
    url = f"https://www.jobstreet.com/{loc_slug}/jobs/{title_slug}-jobs"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("article", {"data-automation": "normalJob"})[:max_results]

        for card in cards:
            try:
                job_title = card.find("a", {"data-automation": "jobTitle"})
                company   = card.find("a", {"data-automation": "jobCompany"})
                loc_el    = card.find("span", {"data-automation": "jobLocation"})
                link      = job_title["href"] if job_title and job_title.get("href") else url

                jobs.append({
                    "title":    job_title.text.strip() if job_title else title,
                    "company":  company.text.strip()   if company   else "Unknown",
                    "location": loc_el.text.strip()    if loc_el    else location,
                    "source":   "JobStreet",
                    "url":      "https://www.jobstreet.com" + link if link.startswith("/") else link,
                })
            except Exception:
                continue

    except Exception as e:
        print(f"[JobStreet] Error scraping '{title}' in '{location}': {e}")

    return jobs


def scrape_linkedin(title: str, location: str, max_results: int = 10) -> list[dict]:
    """Scrape LinkedIn public job listings."""
    jobs = []
    query = urllib.parse.urlencode({
        "keywords": title,
        "location": location,
        "sortBy":   "DD",   # Date descending
        "f_TPR":    "r86400",  # Last 24 hours
    })
    url = f"https://www.linkedin.com/jobs/search/?{query}"

    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        cards = soup.find_all("div", class_="base-card")[:max_results]

        for card in cards:
            try:
                job_title = card.find("h3", class_="base-search-card__title")
                company   = card.find("h4", class_="base-search-card__subtitle")
                loc_el    = card.find("span", class_="job-search-card__location")
                link_tag  = card.find("a", class_="base-card__full-link")

                jobs.append({
                    "title":    job_title.text.strip() if job_title else title,
                    "company":  company.text.strip()   if company   else "Unknown",
                    "location": loc_el.text.strip()    if loc_el    else location,
                    "source":   "LinkedIn",
                    "url":      link_tag["href"]        if link_tag  else url,
                })
            except Exception:
                continue

    except Exception as e:
        print(f"[LinkedIn] Error scraping '{title}' in '{location}': {e}")

    return jobs


def fetch_all_jobs(titles: list, locations: list, max_per_search: int = 10) -> list[dict]:
    """Fetch jobs from all sources for all title+location combos."""
    all_jobs = []

    for title in titles:
        for location in locations:
            print(f"🔍 Searching: '{title}' in '{location}'")

            all_jobs.extend(scrape_indeed(title, location, max_per_search))
            time.sleep(random.uniform(1.5, 3.0))  # polite delay

            all_jobs.extend(scrape_jobstreet(title, location, max_per_search))
            time.sleep(random.uniform(1.5, 3.0))

            all_jobs.extend(scrape_linkedin(title, location, max_per_search))
            time.sleep(random.uniform(1.5, 3.0))

    print(f"✅ Total jobs fetched: {len(all_jobs)}")
    return all_jobs
