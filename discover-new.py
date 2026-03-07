#!/usr/bin/env python3
"""
Auto-discover and add new tools/products from the discovery pool.
Picks 3-5 candidates per run, validates URLs, adds to products.json.
"""

import json
import random
import datetime
import urllib.request
import ssl
import os
import sys


def load_json(path):
    """Load a JSON file with UTF-8 encoding."""
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    """Save a JSON file with UTF-8 encoding, no ASCII escaping."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved: {path}")


def validate_url(url, timeout=15):
    """
    Validate a URL by sending an HTTP HEAD request (fallback to GET).
    Returns True if the URL responds with a success status code.
    """
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    # Try HEAD first
    try:
        req = urllib.request.Request(url, method='HEAD', headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        code = resp.getcode()
        if 200 <= code < 400:
            return True, code
    except Exception:
        pass

    # Fallback to GET
    try:
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        code = resp.getcode()
        if 200 <= code < 400:
            return True, code
    except Exception as e:
        return False, str(e)

    return False, "Unknown error"


def build_product(candidate, today):
    """Convert a discovery-pool candidate into a products.json entry."""
    product = {
        "id": candidate["id"],
        "name": candidate["name"],
        "category": candidate["category"],
        "summary": candidate["summary"],
        "description": candidate["description"],
        "rating": candidate["rating"],
        "price": candidate["price"],
        "affiliateUrl": candidate.get("affiliateUrl", ""),
        "affiliateProvider": candidate.get("affiliateProvider", ""),
        "imageUrl": candidate.get("imageUrl", ""),
        "pros": candidate["pros"],
        "cons": candidate["cons"],
        "features": candidate["features"],
        "officialUrl": candidate["officialUrl"],
        "lastChecked": today,
        "dateAdded": today,
        "status": "active",
        "featured": candidate.get("featured", False),
        "region": candidate.get("region", "global"),
        "tags": candidate.get("tags", [])
    }
    return product


def main():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    products_path = os.path.join(base_dir, 'data', 'products.json')
    pool_path = os.path.join(base_dir, 'data', 'discovery-pool.json')

    today = datetime.date.today().isoformat()
    print(f"=== Product Discovery ({today}) ===")

    # Load data
    products_data = load_json(products_path)
    pool_data = load_json(pool_path)

    existing_ids = set(p['id'] for p in products_data['products'])
    candidates = pool_data['candidates']

    print(f"  Existing products: {len(existing_ids)}")
    print(f"  Pool candidates: {len(candidates)}")

    # Filter unprocessed candidates whose ID is not already in products
    available = [
        c for c in candidates
        if not c.get('processed', False) and c['id'] not in existing_ids
    ]

    if not available:
        print("  Discovery pool exhausted. No new candidates available.")
        return

    print(f"  Available candidates: {len(available)}")

    # Pick up to 5 random unprocessed candidates
    pick_count = min(5, len(available))
    selected = random.sample(available, pick_count)
    print(f"  Selected {pick_count} candidates for processing.")

    added = 0
    failed = 0

    for candidate in selected:
        cid = candidate['id']
        name = candidate['name']
        url = candidate['officialUrl']

        print(f"\n  Processing: {name} ({cid})")
        print(f"    URL: {url}")

        # Validate URL
        ok, result = validate_url(url)

        # Find this candidate in the pool to update it
        pool_entry = next(c for c in candidates if c['id'] == cid)

        if ok:
            print(f"    URL OK (status: {result})")
            # Add to products
            product = build_product(candidate, today)
            products_data['products'].append(product)
            pool_entry['processed'] = True
            added += 1
        else:
            print(f"    URL FAILED: {result}")
            pool_entry['processed'] = True
            pool_entry['failed'] = True
            failed += 1

    # Save updated files
    print(f"\n  Saving updated files...")
    save_json(products_path, products_data)
    save_json(pool_path, pool_data)

    # Summary
    print(f"\n=== Discovery Summary ===")
    print(f"  Processed: {pick_count}")
    print(f"  Added: {added}")
    print(f"  Failed: {failed}")
    print(f"  Total products now: {len(products_data['products'])}")

    remaining = sum(1 for c in candidates if not c.get('processed', False) and c['id'] not in existing_ids)
    print(f"  Remaining in pool: {remaining}")


if __name__ == '__main__':
    main()
