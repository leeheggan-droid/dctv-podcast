#!/usr/bin/env python3
"""Build feed.xml for the DC TV podcast from yt-dlp metadata + audio files."""
import json, os, html, sys
from datetime import datetime, timezone
from email.utils import format_datetime

BASE = "https://leeheggan-droid.github.io/dctv-podcast"
SITE = "https://tv.leeheggan.tech"
VIDS = {1:"BmDiqxGqm9E",2:"E1TW2i-cRcg",3:"yO19xDc7FAE",4:"0KsSjV0Bzp4",5:"JEYKtKi_pYw",
        6:"akokwnTkAHI",7:"MRvijyTC4kw",8:"CMaDyAquzD0",9:"U7VYFyQ782k",10:"CZCu1oxYpI4",
        11:"5k9wb2QdcS8",12:"Rq11yYGmSGU",13:"FLB7u_hjJIg",14:"Xig_F-sxx4E",15:"UBHa00CwaZs"}
ROOT = os.path.dirname(os.path.abspath(__file__))

def clean(s, limit=4000):
    s = (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return s[:limit]

def pubdate(yyyymmdd):
    dt = datetime.strptime(yyyymmdd, "%Y%m%d").replace(tzinfo=timezone.utc)
    return format_datetime(dt)

items = []
errors = []
for n in sorted(VIDS, reverse=True):
    vid = VIDS[n]
    mp3 = f"{ROOT}/audio/ep{n:02d}.mp3"
    mj = f"{ROOT}/meta/{vid}.json"
    if not os.path.isfile(mp3):
        errors.append(f"missing {mp3}"); continue
    meta = json.load(open(mj))
    size = os.path.getsize(mp3)
    title = clean(meta.get("title") or f"DC TV Episode {n}", 250)
    desc = clean(meta.get("description") or f"DC TV episode {n}.")
    items.append(f"""    <item>
      <title>{title}</title>
      <link>https://www.youtube.com/watch?v={vid}</link>
      <guid isPermaLink="false">dctv-ep{n:02d}-{vid}</guid>
      <pubDate>{pubdate(meta['upload_date'])}</pubDate>
      <description>{desc}</description>
      <enclosure url="{BASE}/audio/ep{n:02d}.mp3" length="{size}" type="audio/mpeg"/>
      <itunes:explicit>no</itunes:explicit>
      <itunes:image href="{BASE}/cover.jpg"/>
    </item>""")

if errors:
    print("ERRORS:", errors, file=sys.stderr); sys.exit(1)

feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
  <channel>
    <title>DC TV — APAC Data Centre News</title>
    <link>{SITE}</link>
    <description>The weekly APAC data-centre wrap, AI-presented by DC TV. Editorial claims are sourced and reviewed before publication.</description>
    <language>en</language>
    <lastBuildDate>{format_datetime(datetime.now(timezone.utc))}</lastBuildDate>
    <itunes:author>DC TV</itunes:author>
    <itunes:email>tv@leeheggan.tech</itunes:email>
    <managingEditor>tv@leeheggan.tech (DC TV)</managingEditor>
    <itunes:explicit>no</itunes:explicit>
    <itunes:category text="Technology"/>
    <itunes:image href="{BASE}/cover.jpg"/>
    <image>
      <url>{BASE}/cover.jpg</url>
      <title>DC TV — APAC Data Centre News</title>
      <link>{SITE}</link>
    </image>
{chr(10).join(items)}
  </channel>
</rss>
"""
open(f"{ROOT}/feed.xml", "w").write(feed)
print(f"feed.xml written: {len(items)} items")
