import os
import json
import time
import datetime
import urllib.request
import urllib.parse

# =====================================================================
# ⚙️ إعدادات المنظومة
# =====================================================================
CONFIG = {
    "DOMAIN": "https://giize.com",
    "PAGES_DOMAIN": "https://giize-live.pages.dev",
    "SMARTLINK_URL": "https://www.effectivecpmnetwork.com/ersihz46k6?key=5739767d6e39c4e87b743acd12a17516",
    "INDEXNOW_KEY": "giize_indexnow_key_2026",
    "OUTPUT_DIR": "."
}

# بيانات الحساب الخدمي المعتمد في Google Search Console
SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "fine-bearing-506208-g6",
  "private_key_id": "fa04a7c0aad4dd888fc076368b9020780890dc2f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD7Gr5n8r9eqiGI\nWbGWhCNA2dn99OK6L/1QD3n2pGdZkxQ9PdycfrOkWSg1jad0ZDKLLKXA4RdPtWa5\nlKF74ZSrVWcXaMI4Waj3cfqZr95iG6/Yej3wLvaOOzExOa6fq74+0iPdj4ri7+yw\nqEwGoe33ilWfa/YMyYifqIxRESNfM+zINAjfGXLNA6qKGpwa3VPOf56ZqC0zWjsF\nj9RjkMgVUWyPtM2SfFZoYF7GV9xyhhagA04yoliR5pQshMKlorsyW0hy1fbxaj82\nnyLJ7DGmTjXrNzUkGCsNj+URQCy8Gby47n84RAXI2n+ZEeKl7STvUxbvoRj8fa7z\nBIW4zLYLAgMBAAECggEAOe2mhXaD3YPkLn96r52WQGzBlIu9DnTpvGGFone0+/4p\nSiOOVHAKY1zKIOin+/rtihvntUJ4TUQtCZ0XT+vvj0MpgEYDoFpW15bs2C2xYPLA\nM3Gn/lPnP1K6e3+yIFXPktCJw6BMyyPMd8irmVAcBOJd9GREpBiOMz7/9+e7QEfW\nWaIttah6Jkwr2dFMcDeCrL50s+h1ugBPRgf+vVt0fjW2tPss7ElaIpyGCFMOSYI2\nyvakfSZD9slF9Ufbap5y5OlI3sZ+u/jpKYpiPE+YKBbc6leXt1f4BGcWTdXcY1J2\nT2GbSMqADjd4IGWlFP9PBw6X2qyJyCMfYghbAxiioQKBgQD+Dy4UJSZj7MmYUoyM\nqNRlvmi2GNc3lG/i84VcDdotzPE2Uevt6cpIJbBwkgfAiYbVTe4UO0oGRzMEdIcf\nZgHGoQM1X7P4xeIwaHwU3ey3dIixZopJxvUr5fS+4ErCJ62njdklvNx7ySl9V0sC\nOzb/7stdtKkBsZzOxa+8WwXpOwKBgQD9BckYZ9MPKuScc+qKWTrZKf5mSZAzD3bL\nCQdBvS76KMbOatxL80t0nfmo782eOpGP9+TX1HOdTRoOolZinBk3kBreKQDQU4gb\nOdWTZ5cH32U5Ls2QXtoqI75j7YgDQWwjxEE1v4KMecgZRS8jSegt3lD7mb/rMHLb\nhJ8vv54ZcQKBgBLv5LphroPiQYCWHp3Zc8OFtt5j6Z7d9J0RE86xxaKGVTB8WL6q\nH4bTMFyjteo3FhLONUHSzYi8Q+RAH1ZKzzUUCV4wHQUdEugS0bToed2O1SWMBCDN\nsLat9FlJ9KiWNo53t0jl0/VyICKUoCWxbj8TeJsqfTKAH7UV7Sx4CG/DAoGBAJlo\nQ5e3g2ED2Z3+Ler51NNMQcFUwsgijRzm+W5jPLNRu8/1PGIUPeCT04YY9usDibPn\nUemGFx79W1oaFRQunp9wkMm3xJWKv8/6DcMUoJ6WVLIJ7Xql99Jq34mIv9lxdhZt\nbDghSA7R239u0fisW8hLrYAOpSz8r/bmfvmdTUcRAoGBANvbNJuwwCpS66tCYB+N\nFAdIvT3SRj9e730iaYJEVsteXuF5r66fBpb+B0gia2c+yvtZSINIE55Uoqvq5IEg\ntOGvNVP/yEoij3fCw2a558JVWn7bQABg4djZt3vjZ6nLIMO0mWs5VFQDlYWy6+Wp\nyEWq/OCNWZlBc9eelFoVsoX5\n-----END PRIVATE KEY-----\n",
  "client_email": "indexing-bot@fine-bearing-506208-g6.iam.gserviceaccount.com",
  "token_uri": "https://oauth2.googleapis.com/token"
}

# =====================================================================
# 🌐 جلب مباريات اليوم العالمية من Free Live Video API
# =====================================================================
def fetch_global_matches():
    url = "https://www.scorebat.com/video-api/v3/feed/?token=MTc5NTI5XzE3MjQxNTg0ODhfOGFlN2EzMmQyNGNiMWM5OGFjY2MxNDYwMmIwMDExOTc="
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            matches = []
            for item in data.get("response", []):
                title = item.get("title", "")
                competition = item.get("competition", "")
                match_date = item.get("date", "")
                thumbnail = item.get("thumbnail", "")
                videos = item.get("videos", [])
                embed_html = videos[0].get("embed", "") if videos else ""
                
                embed_url = ""
                if "src='" in embed_html:
                    embed_url = embed_html.split("src='")[1].split("'")[0]
                elif 'src="' in embed_html:
                    embed_url = embed_html.split('src="')[1].split('"')[0]
                else:
                    embed_url = "https://www.scorebat.com/embed/g/123456/"

                slug = title.lower().replace(" ", "-").replace(":", "").replace("/", "-")
                matches.append({
                    "title": title,
                    "league": competition,
                    "date": match_date,
                    "thumbnail": thumbnail,
                    "embed_url": embed_url,
                    "slug": slug
                })
            return matches
    except Exception as e:
        print(f"⚠️ خطأ في جلب المباريات المباشرة: {e}")
        return []

# =====================================================================
# 🔑 دالة استخراج Access Token لجوجل
# =====================================================================
def get_google_access_token():
    try:
        from google.oauth2 import service_account
        import google.auth.transport.requests

        scopes = ["https://www.googleapis.com/auth/indexing"]
        credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_INFO, scopes=scopes)
        request = google.auth.transport.requests.Request()
        credentials.refresh(request)
        return credentials.token
    except Exception as e:
        print(f"⚠️ خطأ توكن جوجل: {e}")
        return None

# =====================================================================
# 🚀 إرسال الأرشفة لجوجل
# =====================================================================
def send_google_indexing(url, token):
    if not token:
        return
    endpoint = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    payload = json.dumps({"url": url, "type": "URL_UPDATED"}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.getcode() == 200:
                print(f"🎯 [Google Indexing API] أرشفة فورية بنجاح ✅ -> {url}")
    except Exception as e:
        print(f"❌ خطأ جوجل: {e}")

# =====================================================================
# ⚡ إرسال الأرشفة لـ IndexNow (Bing / Yahoo / Yandex)
# =====================================================================
def send_indexnow(urls):
    payload = {
        "host": "giize.com",
        "key": CONFIG["INDEXNOW_KEY"],
        "keyLocation": f"{CONFIG['DOMAIN']}/{CONFIG['INDEXNOW_KEY']}.txt",
        "urlList": urls
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=data, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req) as response:
            print(f"🚀 [IndexNow - Bing/Yahoo] تم إرسال {len(urls)} صفحة بنجاح ✅")
    except Exception as e:
        print(f"⚠️ خطأ IndexNow: {e}")

# =====================================================================
# 🛠️ دالة بناء الصفحات والأرشفة
# =====================================================================
def main():
    print("🌍 جاري سحب جدول مباريات العالم الحية...")
    matches = fetch_global_matches()
    print(f"⚽ تم العثور على {len(matches)} مباراة حية متوفرة الآن!")

    os.makedirs(os.path.join(CONFIG["OUTPUT_DIR"], "match"), exist_ok=True)
    generated_urls = []
    today_iso = datetime.datetime.utcnow().isoformat() + "Z"

    # قالب الـ HTML لكل مباراة مستقلة مع السكيما والكلمات المفتاحية والسمارت لينك
    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Watch {title} Live Stream Free HD - {league}</title>
  <meta name="description" content="Watch {title} live stream online in Full HD. Real-time scores, lineups, video stream and commentary for {league} on Giize Sports.">
  <meta name="keywords" content="{title} live stream, watch {title} free online, {league} stream, football live broadcast, soccer live match">

  <!-- Schema Markup for Google Live Broadcast Indexing -->
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BroadcastEvent",
    "name": "{title} Live Broadcast",
    "isLiveBroadcast": true,
    "startDate": "{date}",
    "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
    "eventStatus": "https://schema.org/EventScheduled",
    "video": {{
      "@type": "VideoObject",
      "name": "{title} Live Stream HD",
      "description": "Watch live football stream and real-time coverage for {title}",
      "thumbnailUrl": "{thumb}",
      "uploadDate": "{date}",
      "embedUrl": "https://giize.com/match/{slug}.html"
    }}
  }}
  </script>

  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    body {{ background-color: #0b0e14; color: #e1e7ec; min-height: 100vh; display: flex; flex-direction: column; align-items: center; }}
    header {{ width: 100%; max-width: 1000px; padding: 18px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1a2230; }}
    .logo {{ font-size: 24px; font-weight: 900; color: #00d26a; text-decoration: none; }}
    .live-badge {{ background: #ff3344; color: #fff; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }}
    .container {{ width: 100%; max-width: 1000px; padding: 20px; text-align: center; }}
    .ad-banner-top {{ width: 100%; min-height: 90px; background: #121824; border: 1px dashed #2e3c54; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: center; align-items: center; color: #5a6a80; font-size: 13px; font-weight: bold; }}
    .match-header {{ background: #121824; border-radius: 12px; padding: 20px; margin-bottom: 20px; border: 1px solid #1f2a3d; }}
    .league-name {{ color: #00d26a; font-size: 14px; font-weight: bold; text-transform: uppercase; margin-bottom: 8px; }}
    .teams {{ font-size: 26px; font-weight: 800; color: #fff; }}
    .player-box {{ position: relative; width: 100%; padding-top: 56.25%; background: #000; border-radius: 12px; overflow: hidden; border: 2px solid #1f2a3d; margin-bottom: 20px; }}
    .player-box iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }}
    .servers-grid {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin: 15px 0; }}
    .server-btn {{ background: #1a2230; color: #fff; text-decoration: none; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 14px; border: 1px solid #2e3c54; }}
    .server-btn.active {{ background: #00d26a; color: #000; }}
    .ad-banner-bottom {{ width: 100%; min-height: 250px; background: #121824; border: 1px dashed #2e3c54; border-radius: 8px; margin-top: 25px; display: flex; justify-content: center; align-items: center; color: #5a6a80; font-size: 13px; font-weight: bold; }}
    .seo-box {{ background: #121824; padding: 20px; border-radius: 12px; text-align: left; color: #a0aec0; font-size: 14px; line-height: 1.8; border: 1px solid #1f2a3d; margin-top: 20px; }}
    footer {{ margin-top: auto; padding: 20px; color: #5a6a80; font-size: 13px; text-align: center; width: 100%; border-top: 1px solid #1a2230; }}
  </style>
</head>
<body>
  <header>
    <a href="/" class="logo">GIIZE<span>SPORTS</span></a>
    <span class="live-badge">🔴 LIVE STREAM</span>
  </header>
  <div class="container">
    <div class="ad-banner-top">📢 SPONSOR / BANNER AD SPACE (728x90)</div>
    <div class="match-header">
      <div class="league-name">{league}</div>
      <div class="teams">{title}</div>
    </div>
    <div class="player-box">
      <iframe src="{embed}" allowfullscreen="true" scrolling="no"></iframe>
    </div>
    <div class="servers-grid">
      <a href="{smartlink}" target="_blank" class="server-btn active">⚡ Server 1 (HD Live)</a>
      <a href="{smartlink}" target="_blank" class="server-btn">🚀 Server 2 (4K Ultra)</a>
      <a href="{smartlink}" target="_blank" class="server-btn">🎧 Audio Commentary</a>
    </div>
    <div class="ad-banner-bottom">📢 RESPONSIVE BANNER AD SPACE (300x250)</div>
    <div class="seo-box">
      <h3 style="color:#fff; margin-bottom: 8px;">Live Stream Coverage: {title}</h3>
      <p>Watch free live football stream for <strong>{title}</strong> playing in the <strong>{league}</strong>. High-definition stream with real-time match events, commentary, and full match replay.</p>
    </div>
  </div>
  <footer>&copy; 2026 Giize Sports Network.</footer>
</body>
</html>"""

    # توليد صفحات المباريات
    for m in matches:
        match_html = template.format(
            title=m["title"],
            league=m["league"],
            date=m["date"] if m["date"] else today_iso,
            thumb=m["thumbnail"] if m["thumbnail"] else "https://giize.com/assets/thumb.jpg",
            embed=m["embed_url"],
            slug=m["slug"],
            smartlink=CONFIG["SMARTLINK_URL"]
        )
        file_path = os.path.join(CONFIG["OUTPUT_DIR"], "match", f"{m['slug']}.html")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(match_html)
        
        page_url = f"{CONFIG['DOMAIN']}/match/{m['slug']}.html"
        generated_urls.append(page_url)

    # إنشاء sitemap.xml
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in generated_urls:
        sitemap += f"  <url>\n    <loc>{u}</loc>\n    <changefreq>hourly</changefreq>\n    <priority>0.9</priority>\n  </url>\n"
    sitemap += "</urlset>"

    with open(os.path.join(CONFIG["OUTPUT_DIR"], "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("📋 تم تحديث sitemap.xml بنجاح.")

    # 1. إرسال الأرشفة لجوجل (أول 200 رابط رئيسي)
    token = get_google_access_token()
    if token:
        for u in generated_urls[:200]:
            send_google_indexing(u, token)
            time.sleep(0.5)

    # 2. إرسال الأرشفة لـ IndexNow (لكل الروابط دفعة واحدة بدون سقف)
    if generated_urls:
        send_indexnow(generated_urls)

    print(f"\n🎉 تم الانتهاء! تم توليد وأرشفة {len(generated_urls)} مباراة عالمية.")

if __name__ == "__main__":
    main()
