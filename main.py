import requests
import json
import time
from datetime import datetime
from typing import List

# Simple AI term radar: fetch new repos from GitHub search and extract uncommon terms

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
QUERY = "AI created:>2025-01-01"
HEADERS = {"Accept": "application/vnd.github.v3+json"}

# Minimal stop words to filter meaningful terms
STOP_WORDS = {"ai", "the", "and", "for", "with", "from", "new", "model", "repo", "llm", "data"}

def get_repos() -> list:
    params = {"q": QUERY, "sort": "stars", "order": "desc", "per_page": 10}
    resp = requests.get(GITHUB_SEARCH_URL, headers=HEADERS, params=params)
    if resp.status_code == 200:
        return resp.json().get("items", [])
    return []

def extract_terms(repo_names: List[str]) -> set:
    terms = set()
    for name in repo_names:
        words = name.replace("-", " ").replace("_", " ").split()
        for w in words:
            if len(w) >= 4 and w.lower() not in STOP_WORDS:
                terms.add(w.lower())
    return terms

def main():
    repos = get_repos()
    if not repos:
        print("No repos found")
        return
    names = [r["name"] + " " + (r.get("description") or "") for r in repos]
    terms = extract_terms(names)
    print(f"\nTerm Radar - {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    print("Trending terms from latest AI repos:\n")
    for idx, term in enumerate(sorted(terms)[:20], 1):
        print(f"{idx:2d}. {term}")

if __name__ == "__main__":
    main()
