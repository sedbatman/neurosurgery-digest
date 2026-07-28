#!/usr/bin/env python3
"""
Fetch latest neurosurgery and spine surgery articles from PubMed.
Outputs JSON to _build/articles_data.json
"""
import json, urllib.request, sys, os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
BUILD_DIR = BASE_DIR / "_build"
BUILD_DIR.mkdir(parents=True, exist_ok=True)

PUBMED_SEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

QUERIES = [
    ("spine", "spine+surgery+OR+spinal+fusion+OR+disc+herniation+OR+spinal+stenosis+OR+spinal+deformity"),
    ("neuro-onc", "glioma+OR+glioblastoma+OR+neuro-oncology+OR+brain+tumor+OR+meningioma"),
    ("neuro-vasc", "intracranial+aneurysm+OR+subarachnoid+hemorrhage+OR+stroke+OR+cerebrovascular"),
    ("neuro-trauma", "traumatic+brain+injury+OR+spinal+cord+injury+OR+head+trauma"),
    ("minimally-invasive", "minimally+invasive+spine+OR+endoscopic+spine+OR+MISS+OR+microsurgery"),
]

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "NeurosurgeryDigest/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())

def fetch_xml(url):
    req = urllib.request.Request(url, headers={"User-Agent": "NeurosurgeryDigest/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read().decode("utf-8")

def get_article_ids():
    all_ids = set()
    for label, query in QUERIES:
        url = f"{PUBMED_SEARCH}?db=pubmed&term={query}&reldate=30&datetype=pdat&retmax=8&retmode=json"
        try:
            data = fetch_json(url)
            ids = data.get("esearchresult", {}).get("idlist", [])
            all_ids.update(ids)
        except Exception as e:
            print(f"  Search {label} failed: {e}", file=sys.stderr)
    return list(all_ids)

def summarize_articles(id_list):
    if not id_list:
        return []
    ids = ",".join(id_list)
    url = f"{PUBMED_SUMMARY}?db=pubmed&id={ids}&retmode=json"
    try:
        data = fetch_json(url)
    except Exception as e:
        print(f"  Summary fetch failed: {e}", file=sys.stderr)
        return []
    
    result = data.get("result", {})
    uids = result.get("uids", [])
    
    articles = []
    for uid in uids:
        a = result.get(uid, {})
        doi = ""
        for aid in a.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "")
        authors = [aut.get("name", "") for aut in a.get("authors", [])[:4]]
        
        articles.append({
            "pmid": uid,
            "title": a.get("title", ""),
            "journal": a.get("source", ""),
            "pubdate": a.get("pubdate", ""),
            "doi": doi,
            "authors": ", ".join(authors),
            "pub_types": a.get("pubtype", []),
            "sort_date": a.get("sortpubdate", ""),
        })
    
    return articles

def fetch_abstracts(articles):
    """Fetch abstracts for the best articles."""
    ids = ",".join(a["pmid"] for a in articles[:15])
    xml = fetch_xml(f"{PUBMED_FETCH}?db=pubmed&id={ids}&retmode=xml&rettype=abstract")
    
    import re
    abstracts = {}
    for article in re.findall(r"<PubmedArticle>.*?</PubmedArticle>", xml, re.DOTALL):
        pmid_m = re.search(r"<PMID[^>]*>(\d+)</PMID>", article)
        if not pmid_m:
            continue
        pmid = pmid_m.group(1)
        
        title_m = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", article, re.DOTALL)
        title = re.sub(r"<[^>]+>", "", title_m.group(1)) if title_m else ""
        
        abs_parts = []
        for abs_el in re.findall(r"<AbstractText[^>]*>(.*?)</AbstractText>", article, re.DOTALL):
            abs_parts.append(re.sub(r"<[^>]+>", "", abs_el).strip())
        
        abstracts[pmid] = {
            "abstract": " ".join(abs_parts)[:1000],
            "title": title,
        }
    
    for article in articles:
        if article["pmid"] in abstracts:
            article["abstract"] = abstracts[article["pmid"]].get("abstract", "")
            if not article["title"]:
                article["title"] = abstracts[article["pmid"]].get("title", "")
    
    return articles

def main():
    print("Fetching latest neurosurgery articles from PubMed...", file=sys.stderr)
    
    ids = get_article_ids()
    print(f"Found {len(ids)} articles", file=sys.stderr)
    
    articles = summarize_articles(ids)
    print(f"Summarized {len(articles)} articles", file=sys.stderr)
    
    articles = fetch_abstracts(articles)
    
    # Sort by pubdate (newest first)
    articles.sort(key=lambda x: x.get("sort_date", ""), reverse=True)
    
    output = {
        "fetched_at": __import__("datetime").datetime.now().isoformat(),
        "total": len(articles),
        "articles": articles,
    }
    
    out_path = BUILD_DIR / "articles_data.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(articles)} articles to {out_path}", file=sys.stderr)
    print(json.dumps({"status": "ok", "count": len(articles), "file": str(out_path)}))

if __name__ == "__main__":
    main()