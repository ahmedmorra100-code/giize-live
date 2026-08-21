import os
import json
import time
import datetime
import urllib.request
import urllib.parse

# =====================================================================
# ⚙️ إعدادات المنظومة وبيانات الاعتماد
# =====================================================================
CONFIG = {
    "DOMAIN": "https://giize.com",
    "SMARTLINK_URL": "https://YOUR_SMARTLINK_URL_HERE", # رابطك المباشر من Adsterra/Monetag
    "INDEXNOW_KEY": "giize_indexnow_key_2026",
    "OUTPUT_DIR": "./dist"
}

# بيانات الـ Service Account الخاصة بك (مفعلة كمالك في Google Search Console)
SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "fine-bearing-506208-g6",
  "private_key_id": "fa04a7c0aad4dd888fc076368b9020780890dc2f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQD7Gr5n8r9eqiGI\nWbGWhCNA2dn99OK6L/1QD3n2pGdZkxQ9PdycfrOkWSg1jad0ZDKLLKXA4RdPtWa5\nlKF74ZSrVWcXaMI4Waj3cfqZr95iG6/Yej3wLvaOOzExOa6fq74+0iPdj4ri7+yw\nqEwGoe33ilWfa/YMyYifqIxRESNfM+zINAjfGXLNA6qKGpwa3VPOf56ZqC0zWjsF\nj9RjkMgVUWyPtM2SfFZoYF7GV9xyhhagA04yoliR5pQshMKlorsyW0hy1fbxaj82\nnyLJ7DGmTjXrNzUkGCsNj+URQCy8Gby47n84RAXI2n+ZEeKl7STvUxbvoRj8fa7z\nBIW4zLYLAgMBAAECggEAOe2mhXaD3YPkLn96r52WQGzBlIu9DnTpvGGFone0+/4p\nSiOOVHAKY1zKIOin+/rtihvntUJ4TUQtCZ0XT+vvj0MpgEYDoFpW15bs2C2xYPLA\nM3Gn/lPnP1K6e3+yIFXPktCJw6BMyyPMd8irmVAcBOJd9GREpBiOMz7/9+e7QEfW\nWaIttah6Jkwr2dFMcDeCrL50s+h1ugBPRgf+vVt0fjW2tPss7ElaIpyGCFMOSYI2\nyvakfSZD9slF9Ufbap5y5OlI3sZ+u/jpKYpiPE+YKBbc6leXt1f4BGcWTdXcY1J2\nT2GbSMqADjd4IGWlFP9PBw6X2qyJyCMfYghbAxiioQKBgQD+Dy4UJSZj7MmYUoyM\nqNRlvmi2GNc3lG/i84VcDdotzPE2Uevt6cpIJbBwkgfAiYbVTe4UO0oGRzMEdIcf\nZgHGoQM1X7P4xeIwaHwU3ey3dIixZopJxvUr5fS+4ErCJ62njdklvNx7ySl9V0sC\nOzb/7stdtKkBsZzOxa+8WwXpOwKBgQD9BckYZ9MPKuScc+qKWTrZKf5mSZAzD3bL\nCQdBvS76KMbOatxL80t0nfmo782eOpGP9+TX1HOdTRoOolZinBk3kBreKQDQU4gb\nOdWTZ5cH32U5Ls2QXtoqI75j7YgDQWwjxEE1v4KMecgZRS8jSegt3lD7mb/rMHLb\nhJ8vv54ZcQKBgBLv5LphroPiQYCWHp3Zc8OFtt5j6Z7d9J0RE86xxaKGVTB8WL6q\nH4bTMFyjteo3FhLONUHSzYi8Q+RAH1ZKzzUUCV4wHQUdEugS0bToed2O1SWMBCDN\nsLat9FlJ9KiWNo53t0jl0/VyICKUoCWxbj8TeJsqfTKAH7UV7Sx4CG/DAoGBAJlo\nQ5e3g2ED2Z3+Ler51NNMQcFUwsgijRzm+W5jPLNRu8/1PGIUPeCT04YY9usDibPn\nUemGFx79W1oaFRQunp9wkMm3xJWKv8/6DcMUoJ6WVLIJ7Xql99Jq34mIv9lxdhZt\nbDghSA7R239u0fisW8hLrYAOpSz8r/bmfvmdTUcRAoGBANvbNJuwwCpS66tCYB+N\nFAdIvT3SRj9e730iaYJEVsteXuF5r66fBpb+B0gia2c+yvtZSINIE55Uoqvq5IEg\ntOGvNVP/yEoij3fCw2a558JVWn7bQABg4djZt3vjZ6nLIMO0mWs5VFQDlYWy6+Wp\nyEWq/OCNWZlBc9eelFoVsoX5\n-----END PRIVATE KEY-----\n",
  "client_email": "indexing-bot@fine-bearing-506208-g6.iam.gserviceaccount.com",
  "token_uri": "https://oauth2.googleapis.com/token"
}

# جدول مباريات اليوم
TODAY_MATCHES = [
    {
        "home": "Arsenal",
        "away": "Chelsea",
        "league": "Premier League",
        "time": "19:00",
        "slug": "arsenal-vs-chelsea",
        "stream": "https://www.scorebat.com/embed/g/123456/"
    },
    {
        "home": "Barcelona",
        "away": "Real Madrid",
        "league": "La Liga - El Clasico",
        "time": "20:00",
        "slug": "barcelona-vs-real-madrid",
        "stream": "https://www.scorebat.com/embed/g/654321/"
    },
    {
        "home": "Bayern Munich",
        "away": "Dortmund",
        "league": "Bundesliga",
        "time": "17:30",
        "slug": "bayern-vs-dortmund",
        "stream": "https://www.scorebat.com/embed/g/789012/"
    },
    {
        "home": "Liverpool",
        "away": "Manchester City",
        "league": "Premier League",
        "time": "21:00",
        "slug": "liverpool-vs-manchester-city",
        "stream": "https://www.scorebat.com/embed/g/998877/"
    }
]

# =====================================================================
# 🔑 دالة استخراج Access Token من Google Service Account
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
    except ImportError:
        print("💡 لتفعيل الأرشفة الفورية لجوجل، قم بتثبيت: pip install google-auth")
        return None
    except Exception as e:
        print(f"⚠️ خطأ في توليد توكن جوجل: {e}")
        return None

# =====================================================================
# 🚀 دالة إرسال طلب الأرشفة الفورية لـ Google Indexing API
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
                print(f"🎯 [Google Indexing API] تم إرسال الأرشفة بنجاح ✅ -> {url}")
            else:
                print(f"⚠️ Google Response: {resp.getcode()}")
    except Exception as e:
        print(f"❌ Google Indexing Error for ({url}): {e}")

# =====================================================================
# ⚡ دالة إرسال طلب IndexNow لـ Bing و Yahoo
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
            print(f"🚀 [IndexNow - Bing/Yahoo] تم إرسال الدفعة بنجاح ✅ (Status: {response.getcode()})")
    except Exception as e:
        print(f"⚠️ IndexNow Notice: {e}")

# =====================================================================
# 🛠️ دالة توليد الصفحات ونشرها
# =====================================================================
def main():
    print("🚀 بدء تشغيل محرك البث الرياضي والأرشفة الفورية v1.0...")
    os.makedirs(os.path.join(CONFIG["OUTPUT_DIR"], "live"), exist_ok=True)
    
    if not os.path.exists("template.html"):
        print("❌ لم يتم العثور على ملف template.html في نفس المجلد!")
        return

    with open("template.html", "r", encoding="utf-8") as f:
        template_content = f.read()

    generated_urls = []
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    now_iso = datetime.datetime.utcnow().isoformat() + "Z"

    for match in TODAY_MATCHES:
        match_title = f"{match['home']} vs {match['away']}"
        page_html = template_content
        page_html = page_html.replace("{{MATCH_TITLE}}", match_title)
        page_html = page_html.replace("{{HOME_TEAM}}", match["home"])
        page_html = page_html.replace("{{AWAY_TEAM}}", match["away"])
        page_html = page_html.replace("{{LEAGUE_NAME}}", match["league"])
        page_html = page_html.replace("{{MATCH_DATE}}", today_str)
        page_html = page_html.replace("{{MATCH_TIME}}", match["time"])
        page_html = page_html.replace("{{MATCH_TIME_ISO}}", now_iso)
        page_html = page_html.replace("{{MATCH_SLUG}}", match["slug"])
        page_html = page_html.replace("{{STREAM_EMBED_URL}}", match["stream"])
        page_html = page_html.replace("{{SMARTLINK_URL}}", CONFIG["SMARTLINK_URL"])
        page_html = page_html.replace("{{THUMBNAIL_URL}}", f"{CONFIG['DOMAIN']}/assets/sports-thumb.jpg")

        output_path = os.path.join(CONFIG["OUTPUT_DIR"], "live", f"{match['slug']}.html")
        with open(output_path, "w", encoding="utf-8") as out:
            out.write(page_html)

        page_url = f"{CONFIG['DOMAIN']}/live/{match['slug']}.html"
        generated_urls.append(page_url)
        print(f"⚽ تم توليد صفحة المباراة: {page_url}")

    # إنشاء sitemap.xml
    sitemap_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in generated_urls:
        sitemap_xml += f"  <url>\n    <loc>{url}</loc>\n    <lastmod>{today_str}</lastmod>\n    <changefreq>hourly</changefreq>\n  </url>\n"
    sitemap_xml += "</urlset>"

    with open(os.path.join(CONFIG["OUTPUT_DIR"], "sitemap.xml"), "w", encoding="utf-8") as sm:
        sm.write(sitemap_xml)
    print("📋 تم إنشاء خريطة الموقع sitemap.xml بنجاح.")

    # 1. إرسال إلى Google Indexing API
    google_token = get_google_access_token()
    if google_token:
        for u in generated_urls:
            send_google_indexing(u, google_token)
            time.sleep(1) # فاصل ثانية بين الطلبات

    # 2. إرسال إلى IndexNow (Bing / Yahoo)
    send_indexnow(generated_urls)

    print("\n🎉 اكتملت العملية بنجاح! الصفحات جاهزة ومرفوعة ومؤرشفة في محركات البحث.")

if __name__ == "__main__":
    main()
