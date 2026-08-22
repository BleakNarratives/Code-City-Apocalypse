
# [DNA_TAG]
# ORIGIN: Crostini-Chromebook
# PILLAR: codecity-unified
# DEPS: argparse, collections, datetime, json, logging, os, subprocess, sys
# ROLE: Call local Ollama via curl. No requests library needed.
# AUTHOR: Buffy (Codebuff AI)
# SESSION: 2026-08-22 Bucket 08 DNA Sweep
# TIER: Core (3)
# [/DNA_TAG]

import logging

#!/usr/bin/env python3
# pain_engine.py - Pain Point Extraction & Pattern Recognition
# Takes scraped reviews → extracts pain points → identifies business gaps
# Feeds structured output into dna_evolution and pytch
#
# Usage:
#   python pain_engine.py --input cache/plumbers_in_wichita_kansas_1234.json
#   python pain_engine.py --input cache/plumbers_in_wichita_kansas_1234.json --model deepseek-coder
#   cat cache/plumbers_in_wichita_kansas_1234.json | python pain_engine.py --stdin

import json
import sys
import os
import argparse
import subprocess
from datetime import datetime
from collections import Counter

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "qwen2.5-coder:1.5b"
OLLAMA_URL = "http://localhost:11434/api/generate"
OUTPUT_DIR = os.path.expanduser("~/modmind_unified/automation/pain_points")


# ---------------------------------------------------------------------------
# OLLAMA INTERFACE - talk to your local model
# ---------------------------------------------------------------------------

def ollama_generate(prompt, model=DEFAULT_MODEL, temperature=0.3):
    """
    Call local Ollama via curl. No requests library needed.
    Low temperature = more analytical, less creative.
    """
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024,
            "ctx_size": 2048  # Keep low for Android RAM
        }
    })
    
    cmd = [
        "curl", "-s", "-X", "POST",
        OLLAMA_URL,
        "-H", "Content-Type: application/json",
        "-d", payload,
        "--max-time", "60"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("response", "")
        else:
            logging.info(f"[OLLAMA ERROR] {result.stderr}")
            return None
    except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
        logging.info(f"[OLLAMA TIMEOUT/PARSE] {e}")
        return None


# ---------------------------------------------------------------------------
# PAIN POINT EXTRACTION - per-review analysis
# ---------------------------------------------------------------------------

def extract_pain_points_from_review(review_text, model=DEFAULT_MODEL):
    """
    Send one review to Ollama. Extract structured pain points.
    Returns list of pain point dicts.
    """
    prompt = f"""You are a business analyst. Read this customer review and extract specific pain points.
Output ONLY valid JSON - an array of objects. No explanation, no markdown, just the JSON array.

Each object must have:
  "pain_point": short description of the problem (max 10 words)
  "category": one of [pricing, communication, quality, speed, reliability, accessibility, followup, staff, billing, other]
  "severity": one of [low, medium, high, critical]
  "quote": the relevant part of the review that shows this pain point (exact words from review)

Review:
{review_text}

JSON array:"""

    response = ollama_generate(prompt, model=model)
    if not response:
        return []
    
    # Parse JSON from response - strip any markdown fences
    clean = response.strip()
    clean = clean.replace("```json", "").replace("```", "").strip()
    
    # Find the JSON array in the response
    start = clean.find("[")
    end = clean.rfind("]")
    if start >= 0 and end > start:
        clean = clean[start:end+1]
    
    try:
        pain_points = json.loads(clean)
        if isinstance(pain_points, list):
            return pain_points
        return []
    except json.JSONDecodeError:
        # Fallback: if model doesn't output clean JSON, do basic keyword extraction
        return keyword_fallback(review_text)


def keyword_fallback(review_text):
    """
    If Ollama doesn't return clean JSON, do simple keyword-based extraction.
    No AI needed for this layer.
    """
    categories = {
        "pricing": ["expensive", "overpriced", "cost", "price", "charged", "fee", "money", "worth"],
        "communication": ["didn't call", "no response", "ignored", "didn't hear", "no communication", "ghosted"],
        "quality": ["bad job", "poor quality", "broke", "didn't work", "shoddy", "terrible work", "horrible"],
        "speed": ["took forever", "slow", "waited", "hours", "days", "never showed", "late"],
        "reliability": ["no show", "cancelled", "flaky", "unreliable", "didn't show"],
        "followup": ["never followed up", "no follow up", "didn't come back", "left unfinished"],
        "staff": ["rude", "unprofessional", "attitude", "disrespectful", "condescending"],
        "billing": ["overcharged", "wrong bill", "charged twice", "billing error", "refund"],
    }
    
    text_lower = review_text.lower()
    found = []
    
    for category, keywords in categories.items():
        for kw in keywords:
            if kw in text_lower:
                # Find the sentence containing the keyword
                sentences = review_text.replace(".", ".\n").split("\n")
                quote = next((s.strip() for s in sentences if kw in s.lower()), review_text[:100])
                
                found.append({
                    "pain_point": f"{category} issue detected",
                    "category": category,
                    "severity": "medium",
                    "quote": quote
                })
                break  # One per category
    
    return found


# ---------------------------------------------------------------------------
# PATTERN ENGINE - find recurring issues across all reviews
# ---------------------------------------------------------------------------

def identify_patterns(all_pain_points, model=DEFAULT_MODEL):
    """
    Take all extracted pain points and find the RECURRING patterns.
    This is where business gaps emerge.
    """
    if not all_pain_points:
        return {"patterns": [], "gaps": []}
    
    # First: statistical pattern detection (no AI needed)
    category_counts = Counter(pp["category"] for pp in all_pain_points)
    severity_counts = Counter(pp["severity"] for pp in all_pain_points)
    
    # Group pain points by category
    by_category = {}
    for pp in all_pain_points:
        cat = pp["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(pp)
    
    # Find top categories (the recurring patterns)
    top_categories = category_counts.most_common(5)
    
    # Second: use Ollama to synthesize the patterns into business gaps
    # Feed it a SUMMARY, not raw reviews (keeps context window small)
    summary_input = json.dumps({
        "total_reviews_analyzed": len(set()),  # will be set by caller
        "category_frequency": dict(top_categories),
        "severity_distribution": dict(severity_counts),
        "top_pain_points_by_category": {
            cat: [pp["pain_point"] for pp in points[:3]]  # top 3 per category
            for cat, points in by_category.items()
        }
    }, indent=2)
    
    prompt = f"""You are a business opportunity analyst. Based on this pain point summary from customer reviews, identify actionable business gaps - problems that could be solved with a product or service automation.

Output ONLY valid JSON. No explanation. An object with two arrays:
  "patterns": array of recurring problems (each: "description", "frequency", "affected_category")
  "gaps": array of business opportunities (each: "opportunity", "solves_pain_point", "automation_type", "market_size_estimate" as one of [small, medium, large, massive])

Pain Point Summary:
{summary_input}

JSON:"""

    response = ollama_generate(prompt, model=model)
    
    if response:
        clean = response.strip().replace("```json", "").replace("```", "").strip()
        start = clean.find("{")
        end = clean.rfind("}")
        if start >= 0 and end > start:
            clean = clean[start:end+1]
        
        try:
            result = json.loads(clean)
            # Attach the statistical data too
            result["category_frequency"] = dict(top_categories)
            result["severity_distribution"] = dict(severity_counts)
            return result
        except json.JSONDecodeError:
            pass
    
    # Fallback: return just the statistical analysis
    return {
        "patterns": [
            {"description": f"Recurring {cat} complaints", "frequency": count, "affected_category": cat}
            for cat, count in top_categories
        ],
        "gaps": [
            {"opportunity": f"Automation for {cat} pain points", "solves_pain_point": cat, "automation_type": "tbd", "market_size_estimate": "medium"}
            for cat, count in top_categories if count >= 2
        ],
        "category_frequency": dict(top_categories),
        "severity_distribution": dict(severity_counts)
    }


# ---------------------------------------------------------------------------
# PIPELINE OUTPUT - format for pytch and dna_evolution
# ---------------------------------------------------------------------------

def format_for_pytch(query, reviews, pain_points, patterns):
    """
    Structure the output so pytch_ai_interface.py can consume it directly.
    """
    return {
        "agent": "pain_engine",
        "operation": "pain_point_extraction",
        "status": "complete",
        "query": query,
        "timestamp": datetime.utcnow().isoformat(),
        "duration": 0,  # will be set
        "errors": 0,
        "validation": 0.85,
        # Pytch-specific fields
        "summary": {
            "reviews_analyzed": len(reviews),
            "pain_points_extracted": len(pain_points),
            "patterns_found": len(patterns.get("patterns", [])),
            "gaps_identified": len(patterns.get("gaps", [])),
        },
        "patterns": patterns,
        "top_opportunities": patterns.get("gaps", [])[:3],
        # Raw data for deeper analysis
        "_reviews": reviews,
        "_pain_points": pain_points,
    }


def format_for_dna(patterns):
    """
    Structure as an Automation DNA pattern for dna_evolution.sh to consume.
    """
    return {
        "dna_type": "business_gap",
        "created_at": datetime.utcnow().isoformat(),
        "fitness_score": 0,  # will be scored after validation
        "genome": {
            "patterns": patterns.get("patterns", []),
            "gaps": patterns.get("gaps", []),
            "category_frequency": patterns.get("category_frequency", {}),
        },
        "metadata": {
            "source": "pain_engine",
            "version": "1.0"
        }
    }


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    import time
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="Pain Point Extraction & Pattern Engine")
    parser.add_argument("--input", type=str, help="Scraped reviews JSON file")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Ollama model to use")
    parser.add_argument("--skip-ai", action="store_true", help="Use keyword fallback only (no Ollama needed)")
    parser.add_argument("--output", type=str, help="Output file (default: auto-named)")
    
    args = parser.parse_args()
    
    # Load reviews
    if args.stdin:
        raw = sys.stdin.read()
        data = json.loads(raw)
        reviews = data.get("reviews", data) if isinstance(data, dict) else data
        query = data.get("query", "stdin") if isinstance(data, dict) else "stdin"
    elif args.input:
        with open(args.input, 'r') as f:
            data = json.load(f)
        reviews = data.get("reviews", [])
        query = data.get("query", "unknown")
    else:
        parser.print_help()
        sys.exit(1)
    
    logging.info(f"[PAIN ENGINE] Processing {len(reviews)} reviews for: {query}")
    logging.info(f"[MODEL] {'keyword-fallback' if args.skip_ai else args.model}")
    
    # Extract pain points from each review
    all_pain_points = []
    for i, review in enumerate(reviews):
        logging.info(f"  [{i+1}/{len(reviews)}] Extracting...", end="\r", flush=True)
        
        text = review.get("text", "") if isinstance(review, dict) else str(review)
        if not text or len(text) < 20:
            continue
        
        if args.skip_ai:
            points = keyword_fallback(text)
        else:
            points = extract_pain_points_from_review(text, model=args.model)
        
        # Tag each pain point with source info
        for p in points:
            p["source"] = review.get("source", "unknown") if isinstance(review, dict) else "unknown"
            p["source_query"] = query
        
        all_pain_points.extend(points)
    
    logging.info(f"\n[EXTRACTED] {len(all_pain_points)} pain points from {len(reviews)} reviews")
    
    # Identify patterns and business gaps
    logging.info("[PATTERNS] Analyzing for business gaps...")
    if args.skip_ai:
        # Statistical only
        patterns = identify_patterns(all_pain_points, model=None)
    else:
        patterns = identify_patterns(all_pain_points, model=args.model)
    
    logging.info(f"[GAPS] Found {len(patterns.get('gaps', []))} potential business opportunities")
    
    # Format outputs
    duration = round(time.time() - start_time, 2)
    
    pytch_output = format_for_pytch(query, reviews, all_pain_points, patterns)
    pytch_output["duration"] = duration
    
    dna_output = format_for_dna(patterns)
    
    # Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    import re as re_mod
    safe_name = re_mod.sub(r'[^a-zA-Z0-9_]', '_', query)
    timestamp = int(time.time())
    
    pytch_path = os.path.join(OUTPUT_DIR, f"pytch_{safe_name}_{timestamp}.json")
    dna_path = os.path.join(OUTPUT_DIR, f"dna_{safe_name}_{timestamp}.json")
    
    with open(pytch_path, 'w') as f:
        json.dump(pytch_output, f, indent=2)
    
    with open(dna_path, 'w') as f:
        json.dump(dna_output, f, indent=2)
    
    logging.info(f"\n[SAVED] Pytch input:  {pytch_path}")
    logging.info(f"[SAVED] DNA pattern:  {dna_path}")
    
    # Print pipeline summary
    logging.info("\n--- PIPELINE OUTPUT ---")
    print(json.dumps({
        "stage": "pain_engine",
        "query": query,
        "reviews_in": len(reviews),
        "pain_points": len(all_pain_points),
        "patterns": len(patterns.get("patterns", [])),
        "gaps": len(patterns.get("gaps", [])),
        "pytch_file": pytch_path,
        "dna_file": dna_path,
        "duration_seconds": duration,
        "next_steps": [
            f"python pytch_ai_interface.py {pytch_path}",
            f"# Or feed DNA into evolution: cp {dna_path} ~/modmind_unified/automation/docs/"
        ]
    }, indent=2))


if __name__ == "__main__":
    main()
