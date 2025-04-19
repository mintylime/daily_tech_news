# 🛰️ Cyber & Tech News Feed Aggregator

This project generates a daily curated news feed on **cybersecurity**, **strategic technology**, **AI**, and **digital geopolitics**, using live searches from **Google News RSS** and structured keyword categories.

The feed is displayed as a sortable, lightweight HTML page — perfect for policy analysts, researchers, or anyone tracking tech-related developments across multiple domains.

## 📌 Features

- **Live daily updates** via GitHub Actions (scheduled at 6AM AEST)
- Pulls content using **Google News RSS** across multiple curated categories
- Shows only **last 48 hours** of articles by default; toggle to view older items
- Displays **X of Y** article count to quickly assess freshness
- Fully **sortable** table by date and category
- Automatically deploys to **GitHub Pages** as a public dashboard

## 🗂️ Keyword Categories

Search terms are grouped into structured categories including:

- `Cybersecurity & Threat Activity`
- `Information Operations`
- `Surveillance`
- `Digitally-enabled or Assisted Espionage`
- `Strategic Tech & Resilience`
- `AI & Emerging Technologies`
- `Geopolitics & Tech Strategy`
- `Digital Trade`
- `Big Tech`
- `Small Tech`
- `Governance & Regulation`
- `Australian Tech Innovation`

These are managed in [`search_keywords_tech.json`](search_keywords_tech.json).

## 🛠️ How It Works

1. **Python Script** (`news_scraper.py`) loads search terms, queries Google News RSS feeds for each category.
2. (Tries but fails to) Filters results to those **published within the last 7 days**.
3. Generates an `index.html` file showing articles from the **last 48 hours**, hiding older ones by default.
4. HTML includes JS to allow **sorting** and **toggling** visibility of older results.
5. **GitHub Actions** runs this script daily, commits the new HTML file, and deploys it via GitHub Pages.

## 🚀 Deployment

This project uses:

- [GitHub Actions](https://docs.github.com/en/actions) for scheduled automation
- [GitHub Pages](https://pages.github.com/) to host the news dashboard

### Schedule and Manual Trigger

The action runs automatically **once daily** (6AM AEST) and can also be run manually.

## 📄 Live Demo

See the Github Page associated with this project

## 📦 Requirements (Local Dev)

If running locally:

```bash
pip install beautifulsoup4 lxml


