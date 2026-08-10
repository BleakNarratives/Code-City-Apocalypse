import logging

#!/usr/bin/env python3
# scraper.py - Review Pain Point Scraper
# Pulls reviews from BBB, Yelp, Google Business, CFPB
# Extracts and structures pain points for the DNA pipeline
#
# Usage:
#   python scraper.py --source yelp --query "plumbers in wichita kansas"
#   python scraper.py --source all --query "auto repair kansas city"
#   python scraper.py --file reviews.json  (process already-collected reviews)

import json
import sys
import argparse
import subprocess
import re
import os
from datetime import datetime
from urllib.parse import quote

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
OLLAMA_MODEL = "qwen2.5-coder:1.5b"  # or whatever you have loaded
OUTPUT_DIR = os.path.expanduser("~/modmind_unified/automation/scraped")
CACHE_DIR = os.path.expanduser("~/modmind_unified/automation/cache")

# ---------------------------------------------------------------------------
# SCRAPE LAYER - pulls raw review text via curl
# ---------------------------------------------------------------------------

def scrape_yelp(query):
    """
    Yelp doesn't have a free API anymore but we can scrape search results.
    Uses curl + basic HTML parsing. No selenium needed.
    """
    encoded = quote(query)
    url = f"https://www.yelp.com/search?find_desc={encoded}"
    
    raw = curl_fetch(url)
    if not raw:
        return []
    
    # Pull review snippets - Yelp wraps them in specific patterns
    reviews = re.findall(
        r'class="[^"]*review-text[^"]*"[^>]*>(.*?)</span>',
        raw, re.DOTALL
    )
    # Also grab star ratings near reviews
    stars = re.findall(
        r'aria-label="rated (\d+) out of 5 stars"',
        raw
    )
    
    results = []
    for i, review in enumerate(reviews):
        clean = re.sub(r'<[^>]+>', '', review).strip()
        if len(clean) > 20:  # skip fragments
            results.append({
                "source": "yelp",
                "text": clean,
                "stars": int(stars[i]) if i < len(stars) else None,
                "query": query,
                "scraped_at": datetime.utcnow().isoformat()
            })
    
    return results


def scrape_bbb(query):
    """
    Better Business Bureau - scrape complaint summaries.
    BBB complaints are public and structured.
    """
    encoded = quote(query)
    url = f"https://www.bbb.org/us/search?query={encoded}"
    
    raw = curl_fetch(url)
    if not raw:
        return []
    
    # BBB complaint text patterns
    complaints = re.findall(
        r'complaint-summary[^>]*>(.*?)</div>',
        raw, re.DOTALL
    )
    
    results = []
    for complaint in complaints:
        clean = re.sub(r'<[^>]+>', '', complaint).strip()
        if len(clean) > 20:
            results.append({
                "source": "bbb",
                "text": clean,
                "type": "complaint",
                "query": query,
                "scraped_at": datetime.utcnow().isoformat()
            })
    
    return results


def scrape_cfpb(query):
    """
    CFPB has an actual API. Consumer Financial Protection Bureau.
    https://api.consumerfinance.gov/v1/complaints
    Public, no key needed.
    """
    # CFPB API - real, public, structured
    url = f"https://api.consumerfinance.gov/v1/complaints?search_text={quote(query)}&size=25&sort_by=date_received&sort_order=DESC"
    
    raw = curl_fetch(url)
    if not raw:
        return []
    
    try:
        data = json.loads(raw)
        hits = data.get("hits", {}).get("hits", [])
        
        results = []
        for hit in hits:
            src = hit.get("_source", {})
            narrative = src.get("consumer_complaint_narrative", "")
            if narrative and len(narrative) > 30:
                results.append({
                    "source": "cfpb",
                    "text": narrative,
                    "company": src.get("company", ""),
                    "product": src.get("product", ""),
                    "issue": src.get("issue", ""),
                    "state": src.get("state", ""),
                    "date": src.get("date_received", ""),
                    "query": query,
                    "scraped_at": datetime.utcnow().isoformat()
                })
        
        return results
    
    except json.JSONDecodeError:
        return []


def scrape_google_business(query):
    """
    Google Business reviews aren't directly scrapeable without
    hitting rate limits hard. We use a proxy approach:
    Search Google for "[business] reviews" and pull snippet text.
    
    Better long-term: integrate with a reviews API if budget allows.
    """
    encoded = quote(f"{query} reviews")
    url = f"https://www.google.com/search?q={encoded}"
    
    raw = curl_fetch(url)
    if not raw:
        return []
    
    # Google review snippets appear in specific div patterns
    snippets = re.findall(
        r'"snippet"\s*:\s*"(.*?)"',
        raw
    )
    # Also try the newer pattern
    snippets += re.findall(
        r'class="[^"]*BvNj[^"]*"[^>]*>(.*?)</div>',
        raw, re.DOTALL
    )
    
    results = []
    for snippet in snippets:
        clean = re.sub(r'<[^>]+>', '', snippet).strip()
        clean = clean.replace('\\n', ' ').strip()
        if len(clean) > 25:
            results.append({
                "source": "google",
                "text": clean,
                "query": query,
                "scraped_at": datetime.utcnow().isoformat()
            })
    
    return results


def curl_fetch(url):
    """
    Fetch URL via curl. Works in Termux, no pip dependencies needed.
    Rotates a basic user-agent to avoid instant blocks.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    ]
    import random
    ua = random.choice(user_agents)
    
    cmd = [
        "curl", "-s", "-L",
        "--max-time", "15",
        "-A", ua,
        "-H", "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "-H", "Accept-Language: en-US,en;q=0.5",
        url
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        if result.returncode == 0:
            return result.stdout
        return None
    except subprocess.TimeoutExpired:
        logging.info(f"[TIMEOUT] {url}")
        return None


# ---------------------------------------------------------------------------
# ORCHESTRATOR - runs all scrapers, dedupes, caches
# ---------------------------------------------------------------------------

def scrape_all(query):
    """Run all scrapers for a query, combine results"""
    logging.info(f"[SCRAPING] Query: {query}")
    
    all_reviews = []
    
    sources = {
        "yelp": scrape_yelp,
        "bbb": scrape_bbb,
        "cfpb": scrape_cfpb,
        "google": scrape_google_business,
    }
    
    for name, fn in sources.items():
        logging.info(f"  [→] {name}...", end=" ", flush=True)
        try:
            results = fn(query)
            logging.info(f"{len(results)} reviews")
            all_reviews.extend(results)
        except Exception as e:
            logging.info(f"ERROR: {e}")
    
    # Dedupe by text similarity (simple: exact match after normalization)
    seen = set()
    deduped = []
    for r in all_reviews:
        key = r["text"].lower().strip()[:100]
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    
    logging.info(f"\n[TOTAL] {len(all_reviews)} raw → {len(deduped)} deduped")
    return deduped


def scrape_single(source, query):
    """Run one specific scraper"""
    sources = {
        "yelp": scrape_yelp,
        "bbb": scrape_bbb,
        "cfpb": scrape_cfpb,
        "google": scrape_google_business,
    }
    
    if source not in sources:
        logging.info(f"Unknown source: {source}. Options: {list(sources.keys())}")
        return []
    
    logging.info(f"[SCRAPING] {source}: {query}")
    return sources[source](query)


# ---------------------------------------------------------------------------
# SAVE / LOAD
# ---------------------------------------------------------------------------

def save_reviews(reviews, query):
    """Save scraped reviews to cache for the pipeline"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    
    # Filename from query
    safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', query)
    filepath = os.path.join(CACHE_DIR, f"{safe_name}_{int(datetime.utcnow().timestamp())}.json")
    
    payload = {
        "query": query,
        "scraped_at": datetime.utcnow().isoformat(),
        "count": len(reviews),
        "reviews": reviews
    }
    
    with open(filepath, 'w') as f:
        json.dump(payload, f, indent=2)
    
    logging.info(f"\n[SAVED] {filepath}")
    return filepath


def load_reviews(filepath):
    """Load previously scraped reviews"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get("reviews", [])


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Review Pain Point Scraper")
    parser.add_argument("--source", choices=["yelp", "bbb", "cfpb", "google", "all"], default="all")
    parser.add_argument("--query", type=str, help="Business type + location")
    parser.add_argument("--file", type=str, help="Load from existing JSON instead of scraping")
    parser.add_argument("--output", type=str, help="Output file path (default: auto-named in cache)")
    
    args = parser.parse_args()
    
    if args.file:
        # Load mode
        reviews = load_reviews(args.file)
        logging.info(f"[LOADED] {len(reviews)} reviews from {args.file}")
    elif args.query:
        # Scrape mode
        if args.source == "all":
            reviews = scrape_all(args.query)
        else:
            reviews = scrape_single(args.source, args.query)
    else:
        parser.print_help()
        sys.exit(1)
    
    # Save
    if reviews:
        outpath = save_reviews(reviews, args.query or "loaded")
        
        # Print summary for piping into next stage
        logging.info("\n--- PIPELINE OUTPUT ---")
        print(json.dumps({
            "stage": "scraper",
            "query": args.query or "loaded",
            "count": len(reviews),
            "output_file": outpath,
            "sources": list(set(r["source"] for r in reviews))
        }, indent=2))
    else:
        logging.info("\n[EMPTY] No reviews collected. Try a different query or check network.")


if __name__ == "__main__":
    main()
