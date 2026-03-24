#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import numpy as np
import json
from pathlib import Path
from sentence_transformers import SentenceTransformer
from datetime import datetime, timezone


# In[2]:


USER_AGENT = os.getenv(
    "USER_AGENT",
    "TourGuideAI/1.0 (Learning project), Mozilla/5.0 (Windows NT 10.0; Win64; x64), Chrome/91.0.4472.124 Safari/537.36")


# In[3]:


BASE = "https://www.spreewald-info.de"
headers = {"User-Agent": USER_AGENT}

# Links sammeln: Es gibt mehrere Seiten mit Bootsverleih, die alle unter "/paddeln/bootsverleih/" liegen.
url = BASE + "/paddeln/bootsverleih/"
resp = requests.get(url, headers=headers, timeout=20)
resp.raise_for_status()
html = resp.text
soup = BeautifulSoup(html, "html.parser")

links = []

for a in soup.select("a"): #alle Links auf der Seite durchgehen
    href = a.get("href")
    if href.startswith("/paddeln/bootsverleih/") and href != "/paddeln/bootsverleih/":
        links.append(urljoin(BASE, href))
    # if href and "/paddeln/bootsverleih/" in href and href.count("/") >= 3:
    #     links.append(urljoin(BASE, href))

links = list(set(links)) #Duplikate entfernen

for i, link in enumerate(links, start=1):
     print(f"{i}. {link}")


# In[4]:


# Daten extrahieren
def parse_prices(url):

    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    html = resp.text
    soup = BeautifulSoup(html, "html.parser")

    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    prices = []

    for li in soup.select(".anbieterDetailsInfobox li"):
        text = " ".join(li.stripped_strings)
        if "Euro" in text or "€" in text:
            prices.append(text)

    return {
        "anbieter": title,
        "url": url,
        "preise": prices
    }


def fetch_prices_live(source_url: str) -> dict:
    # Holt aktuelle Preise live von der Quellseite
    return parse_prices(source_url)


# In[5]:


# Alle Anbieter und Preise sammeln. parce_prices() ist widerverwendbar
docs = []

for link in links:
    try:
        data = parse_prices(link)
        docs.append(data)

        print("\nAnbieter:", data["anbieter"])
        print("URL:", data["url"])

        for p in data["preise"]:
            print("  -", p)

    except Exception as e:
        print("Fehler bei:", link)
        print(e)


print("\nGesamt Anbieter gescraped:", len(docs))


# In[6]:


#JSON für RAG vorbereiten. Die Preise können sich ändern, deswegen werden nicht direckt in den Text stehen

output_path = Path("providers.jsonl")
retrieved_at = datetime.now(timezone.utc).isoformat()

with output_path.open("w", encoding="utf-8") as f:
    for item in docs:
       #text feld für Embeddings vorbereiten
        text_parts = []
        anbieter = item.get("anbieter", "")
        preise = item.get("preise", "")
        source_url = item.get("url", "")
        text = (
            f"Anbieter: {anbieter}\n"
            f"Leistung: Bootsverleih\n"
            f"Hinweis: Aktuelle Preise bitte über die Quelle abrufen."
        ).strip()

        doc_entry = {
            "id": source_url,
            "text": text,
            "metadata": {
                "source_url": source_url,
                "anbieter": anbieter,
                "license": "unknown",
                "retrieved_at": retrieved_at,
            }
        }

        f.write(json.dumps(doc_entry, ensure_ascii=False) + "\n")


# In[7]:


#test
if docs:
    sample = docs[0]
    live = fetch_prices_live(sample["url"])
    print("\n Anbieter:", live.get("anbieter"))
    print(" Preise :")
    for p in (live.get("preise") or []):
        print(" -", p)


# In[8]:


# embedding
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

data = []

with open("providers.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        data.append(item)
print(f"{len(data)} Dokumente geladen.")


# In[9]:


texts = [item['text'] for item in data]

embeddings_preise = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings_preise).astype('float32')
print(f"Embeddings für {len(embeddings)} Dokumente erstellt.")


# In[10]:


def get_bootsverleih_prices():
    texts = []

    for d in docs:
        name = d["anbieter"]
        url = d["url"]

        # Preise echtzeitig abrufen
        live_data = fetch_prices_live(url)
        prices = live_data.get("preise", [])

        price_text = "\n".join(f"- {p}" for p in prices) if prices else "Keine Preise gefunden."
        texts.append(f"Anbieter: {name}\nPreise:\n{price_text}\nQuelle: {url}")
    return "\n\n".join(texts)

