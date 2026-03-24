#!/usr/bin/env python
# coding: utf-8

# 

# In[1]:


import os
import requests
from typing import Dict, Any

USER_AGENT = os.getenv(
    "USER_AGENT",
    "TourGuideAI/1.0 (Learning project), Mozilla/5.0 (Windows NT 10.0; Win64; x64), Chrome/91.0.4472.124 Safari/537.36")

def search_place(query: str) -> Dict[str, Any]:
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": query,
        "format": "json",
        "limit": 1,
        "addressdetails": 1
    }
    headers = {"User-Agent": USER_AGENT}

    r = requests.get(url, params=params, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    if not data:
        return {}

    return {
        "name": data[0]["display_name"],
        "lat": float(data[0]["lat"]),
        "lon": float(data[0]["lon"]),
        "city": data[0]["address"].get("city") or data[0]["address"].get("town"),
        "state": data[0]["address"].get("state"),
        "country": data[0]["address"].get("country")
    }


def get_museums_opening_hours(lat: float, lon: float, radius: int = 10000):

    query = f"""
    [out:json][timeout:25];

    (
      node["tourism"="museum"](around:{radius},{lat},{lon});
      way["tourism"="museum"](around:{radius},{lat},{lon});
      relation["tourism"="museum"](around:{radius},{lat},{lon});
    );

    out tags center;
    """

    r = requests.post(
        "https://overpass-api.de/api/interpreter",
        data=query,
        headers={"User-Agent": USER_AGENT},
        timeout=60
    )

    r.raise_for_status()
    data = r.json()

    museums = []

    for el in data.get("elements", []):
        tags = el.get("tags", {})

        if not tags.get("name"):
            continue

        lat_val = el.get("lat") or el.get("center", {}).get("lat")
        lon_val = el.get("lon") or el.get("center", {}).get("lon")

        museums.append({
            "name": tags.get("name"),
            "opening_hours": tags.get("opening_hours"),
            "lat": lat_val,
            "lon": lon_val,
            "street": tags.get("addr:street"),
            "housenumber": tags.get("addr:housenumber"),
            "postcode": tags.get("addr:postcode"),
            "city": tags.get("addr:city")
        })

    return museums


# In[2]:


place = search_place("Raddusch, Brandenburg, Deutschland")

if place:
    museums = get_museums_opening_hours(place["lat"], place["lon"])

    for i, m in enumerate(museums, start=1):
        adress = " ".join(filter(None, [m.get("street"), m.get("housenumber"), m.get("postcode"), m.get("city")]))


        print( f" {i} --------------------")
        print (f"   Name: {m.get('name')}")
        print( f"   Öffnungszeiten: {m.get('opening_hours') or 'Keine Informationen verfügbar'}")
        print (f"   Adresse: {adress}")


# In[3]:


#context für LLM+RAG

def get_osm_context(query):
    place = search_place(query)

    if not place:
        return f"Keine Informationen zu {query} gefunden."

    museums = get_museums_opening_hours(place["lat"], place["lon"])

    texts = []
    for m in museums:
        texts.append(
            f"Name: {m.get('name')}\n"
            f"Öffnungszeiten: {m.get('opening_hours') or 'Keine Informationen verfügbar'}\n"
            f"Adresse: {adress}\n"
        )

