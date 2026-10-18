#!/usr/bin/env python3
"""
Run this script whenever you update your Google Sheet:
    python3 export.py

It downloads the sheet and saves songs.json next to this file.
Then redeploy: npx vercel --prod
"""

import csv
import json
import urllib.request
import urllib.error
import sys

SHEET_URL = (
    "https://docs.google.com/spreadsheets/d/"
    "1ShDBKh_sb92hmRhc5YYUdWb_gAhcfyAC/export?format=csv&gid=1901156245"
)

OUTPUT = "songs.json"

def fetch_csv(url):
    print("Downloading sheet...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        return resp.read().decode("utf-8")

def parse(text):
    songs = []
    reader = csv.reader(text.splitlines())
    next(reader)  # skip header
    for i, row in enumerate(reader):
        if len(row) < 3:
            continue
        artist = row[0].strip()
        number = row[1].strip()
        title  = row[2].strip()
        lyrics = row[3].strip() if len(row) > 3 else ""
        idioma = row[4].strip() if len(row) > 4 else ""
        if not artist or not number or not title:
            continue
        category = (
            "nacionais"      if idioma == "BRA" else
            "japonesas"      if idioma == "JAP" else
            "internacionais"
        )
        songs.append({
            "id":       i,
            "artist":   artist,
            "number":   number,
            "title":    title,
            "lyrics":   lyrics,
            "category": category,
        })
    return songs

def main():
    try:
        text  = fetch_csv(SHEET_URL)
        songs = parse(text)
        with open(OUTPUT, "w", encoding="utf-8") as f:
            json.dump(songs, f, ensure_ascii=False, separators=(",", ":"))
        print(f"Done — {len(songs)} songs saved to {OUTPUT}")
    except urllib.error.HTTPError as e:
        print(f"Error fetching sheet: HTTP {e.code}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
