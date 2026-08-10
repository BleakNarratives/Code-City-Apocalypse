import logging

#!/usr/bin/env python3
# scraper.py v2 — Review Pain Point Scraper
# Merged from hybrid_complaints.py + pipeline output format
#
# SOURCES:
#   CFPB          — public API, no key, WORKS
#   Yelp Fusion   — free tier 5000 req/mo, needs YELP_API_KEY
#   Google Places — free tier, needs GOOGLE_PLACES_KEY
#   BBB           — scrape attempt, hit or miss
#
# SETUP:
#   export YELP_API_KEY="your_key"          # yelp.com/developers
#   export GOOGLE_PLACES_KEY="your_key"     # console.cloud.google.com
#
# USAGE:
#   python scraper.py --query "Chase Bank"
#   python scraper.py --query "plumbers kansas city" --source yelp
#   python scraper.py --source all --query "auto repair wichita"
#   python scraper.py --file cache/something.json

import json, sys, os, argparse, subprocess, re, random
from datetime import datetime
from urllib.parse import quote

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
CACHE_DIR = os.path.expanduser("~/modmind_unified/automation/cache")
YELP_KEY   = os.environ.get("YELP_API_KEY", "")
GOOGLE_KEY = os.environ.get("GOOGLE_PLACES_KEY", "")

UA_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
]

# ---------------------------------------------------------------------------
# CURL — everything goes through here. No pip needed.
# ---------------------------------------------------------------------------
def curl(url, headers=None, timeout=20):
    cmd = ["curl", "-s", "-L", "--max-time", str(timeout),
           "-A", random.choice(UA_LIST),
           "-H", "Accept: application/json, text/html;q=0.9, */*;q=0.8",
           "-H", "Accept-Language: en-US,en;q=0.5"]
    if headers:
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
    cmd.append(url)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout+5)
        return r.stdout if r.returncode == 0 and r.stdout.strip() else None
    except subprocess.TimeoutExpired:
        logging.info(f"    [TIMEOUT] {url[:80]}...")
        return None

def curl_json(url, headers=None):
    raw = curl(url, headers=headers)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        logging.info(f"    [JSON ERR] {e}")
        return None

# ---------------------------------------------------------------------------
# CFPB — no key needed. Your guaranteed source.
# ---------------------------------------------------------------------------
def scrape_cfpb(query):
    url = (f"https://api.consumerfinance.gov/v1/complaints"
           f"?search_text={quote(query)}&size=25&sort_by=date_received&sort_order=DESC")
    data = curl_json(url)

    # Fallback endpoint if primary returns nothing
    if not data:
        url2 = (f"https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/"
                f"?company={quote(query)}&size=25")
        data = curl_json(url2)

    if not data:
        return []

    results = []
    for hit in data.get("hits", {}).get("hits", []):
        src = hit.get("_source", {})
        narrative = src.get("consumer_complaint_narrative", "")
        if not narrative or len(narrative) < 30:
            continue
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

# ---------------------------------------------------------------------------
# YELP FUSION — real API. Search → reviews per business.
# ---------------------------------------------------------------------------
def scrape_yelp(query):
    if not YELP_KEY:
        logging.info("    [YELP] No key. export YELP_API_KEY=xxx")
        logging.info("    [YELP] Free signup: https://www.yelp.com/developers/documentation/v3/get_started")
        return []

    headers = {"Authorization": f"Bearer {YELP_KEY}"}

    # Search businesses
    data = curl_json(
        f"https://api.yelp.com/v3/businesses/search?term={quote(query)}&limit=5",
        headers=headers
    )
    if not data or "businesses" not in data:
        logging.info(f"    [YELP] No businesses for: {query}")
        return []

    businesses = data["businesses"]
    logging.info(f"    [YELP] {len(businesses)} businesses found, pulling reviews...")

    # Pull reviews for each
    all_reviews = []
    for biz in businesses:
        biz_id  = biz.get("id")
        biz_name = biz.get("name", "unknown")

        rev_data = curl_json(
            f"https://api.yelp.com/v3/businesses/{biz_id}/reviews?limit=20",
            headers=headers
        )
        if not rev_data or "reviews" not in rev_data:
            continue

        for rev in rev_data["reviews"]:
            text = rev.get("text", "")
            if len(text) < 20:
                continue
            all_reviews.append({
                "source": "yelp",
                "text": text,
                "stars": rev.get("rating"),
                "business": biz_name,
                "business_id": biz_id,
                "query": query,
                "scraped_at": datetime.utcnow().isoformat()
            })

    return all_reviews

# ---------------------------------------------------------------------------
# GOOGLE PLACES — find place → pull reviews.
# ---------------------------------------------------------------------------
def scrape_google(query):
    if not GOOGLE_KEY:
        logging.info("    [GOOGLE] No key. export GOOGLE_PLACES_KEY=xxx")
        logging.info("    [GOOGLE] https://console.cloud.google.com → Enable Places API")
        return []

    # Find place
    data = curl_json(
        f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        f"?input={quote(query)}&inputtype=textquery&fields=place_id,name,rating&key={GOOGLE_KEY}"
    )
    if not data or data.get("status") != "OK" or not data.get("candidates"):
        logging.info(f"    [GOOGLE] No place found: {query}")
        return []

    results = []
    for candidate in data["candidates"][:3]:
        place_id  = candidate.get("place_id")
        place_name = candidate.get("name", "unknown")

        detail = curl_json(
            f"https://maps.googleapis.com/maps/api/place/details/json"
            f"?place_id={place_id}&fields=review,name&key={GOOGLE_KEY}"
        )
        if not detail or detail.get("status") != "OK":
            continue

        for rev in detail.get("result", {}).get("reviews", []):
            text = rev.get("text", "")
            if len(text) < 20:
                continue
            results.append({
                "source": "google",
                "text": text,
                "stars": rev.get("rating"),
                "business": place_name,
                "query": query,
                "scraped_at": datetime.utcnow().isoformat()
            })
    return results

# ---------------------------------------------------------------------------
# BBB — no API. Scrape attempt. Zero is normal.
# ---------------------------------------------------------------------------
def scrape_bbb(query):
    raw = curl(f"https://www.bbb.org/us/search?query={quote(query)}")
    if not raw:
        return []

    results = []
    patterns = [
        r'complaint-summary[^>]*>(.*?)</div>',
        r'class="[^"]*complaint[^"]*"[^>]*>(.*?)</div>',
        r'"complaintText"\s*:\s*"(.*?)"',
        r'"reviewText"\s*:\s*"(.*?)"',
        r'class="[^"]*review[^"]*text[^"]*"[^>]*>(.*?)</(?:div|span|p)>',
    ]
    for pattern in patterns:
        for match in re.findall(pattern, raw, re.DOTALL):
            clean = re.sub(r'<[^>]+>', '', match).strip()
            if len(clean) > 20:
                results.append({
                    "source": "bbb", "text": clean, "type": "complaint",
                    "query": query, "scraped_at": datetime.utcnow().isoformat()
                })
    return results

# ---------------------------------------------------------------------------
# ORCHESTRATOR
# ---------------------------------------------------------------------------
SOURCE_MAP = {"cfpb": scrape_cfpb, "yelp": scrape_yelp, "google": scrape_google, "bbb": scrape_bbb}

def scrape_all(query):
    logging.info(f"\n[SCRAPING] {query}\n")
    logging.info(f"  CFPB:   always on")
    logging.info(f"  Yelp:   {'✓ key' if YELP_KEY else '✗ no key'}")
    logging.info(f"  Google: {'✓ key' if GOOGLE_KEY else '✗ no key'}")
    logging.info(f"  BBB:    scrape attempt\n")

    all_reviews = []
    for name, fn in SOURCE_MAP.items():
        logging.info(f"  [→] {name}...", flush=True)
        try:
            r = fn(query)
            logging.info(f"      → {len(r)}")
            all_reviews.extend(r)
        except Exception as e:
            logging.info(f"      ERROR: {e}")

    # Dedupe
    seen, deduped = set(), []
    for r in all_reviews:
        key = r["text"].lower().strip()[:120]
        if key not in seen:
            seen.add(key)
            deduped.append(r)

    logging.info(f"\n[TOTAL] {len(all_reviews)} raw → {len(deduped)} deduped")
    return deduped

def scrape_one(source, query):
    if source not in SOURCE_MAP:
        logging.info(f"Options: {list(SOURCE_MAP.keys())}")
        return []
    logging.info(f"\n[SCRAPING] {source}: {query}\n")
    return SOURCE_MAP[source](query)

# ---------------------------------------------------------------------------
# SAVE / LOAD
# ---------------------------------------------------------------------------
def save(reviews, query):
    os.makedirs(CACHE_DIR, exist_ok=True)
    safe = re.sub(r'[^a-zA-Z0-9_]', '_', query)
    path = os.path.join(CACHE_DIR, f"{safe}_{int(datetime.utcnow().timestamp())}.json")
    with open(path, 'w') as f:
        json.dump({"query": query, "scraped_at": datetime.utcnow().isoformat(),
                   "count": len(reviews), "reviews": reviews}, f, indent=2)
    return path

def load(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data.get("reviews", []), data.get("query", "unknown")

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Scraper v2")
    parser.add_argument("--source", choices=list(SOURCE_MAP.keys())+["all"], default="all")
    parser.add_argument("--query", type=str)
    parser.add_argument("--file", type=str)
    args = parser.parse_args()

    if args.file:
        reviews, query = load(args.file)
        logging.info(f"[LOADED] {len(reviews)} reviews from {args.file}")
    elif args.query:
        reviews = scrape_all(args.query) if args.source == "all" else scrape_one(args.source, args.query)
        query = args.query
    else:
        parser.print_help()
        sys.exit(1)

    if reviews:
        outpath = save(reviews, query)
        logging.info(f"\n[SAVED] {outpath}")
        logging.info("\n--- PIPELINE OUTPUT ---")
        print(json.dumps({
            "stage": "scraper", "query": query, "count": len(reviews),
            "output_file": outpath,
            "sources": list(set(r["source"] for r in reviews)),
            "next": f"python pain_engine.py --input {outpath}"
        }, indent=2))
    else:
        logging.info("\n[EMPTY] No reviews.\n")
        logging.info("  CFPB zero?   Use company names: 'AT&T' not 'telecom'")
        logging.info("  Yelp/Google? Set API keys (see comments at top)")
        logging.info("  BBB zero?    Normal. No API. Move on.")

if __name__ == "__main__":
    main()
