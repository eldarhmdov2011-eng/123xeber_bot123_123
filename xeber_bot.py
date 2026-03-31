import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import re

def xeberleri_getir():
    saytlar = {
        "Oxu.az": "https://oxu.az",
        "Qafqazinfo": "https://qafqazinfo.az",
        "Report.az": "https://report.az"
    }
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    yeni_siyahi = []
    
    for ad, url in saytlar.items():
        try:
            response = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(response.text, "html.parser")
            
            count = 0
            # Hər sayt üçün fərqli axtarış məntiqi
            if "oxu.az" in url:
                items = soup.find_all("div", class_="news-i")
                for item in items:
                    link = item.find("a", class_="news-i-inner")
                    title = item.find("div", class_="title")
                    if link and title and count < 30:
                        yeni_siyahi.append(f"<li><small style='color:#0057b7'>[{ad}]</small> <a href='https://oxu.az{link.get('href')}' target='_blank'>{title.text.strip()}</a></li>")
                        count += 1
            
            elif "qafqazinfo.az" in url:
                items = soup.find_all("a", class_="news-link") # Nümunə class
                for item in items:
                    if item and count < 30:
                        yeni_siyahi.append(f"<li><small style='color:#0057b7'>[{ad}]</small> <a href='{item.get('href')}' target='_blank'>{item.text.strip()}</a></li>")
                        count += 1

            elif "report.az" in url:
                items = soup.find_all("a", class_="news-title") # Nümunə class
                for item in items:
                    if item and count < 30:
                        href = item.get('href')
                        full_href = href if href.startswith("http") else "https://report.az" + href
                        yeni_siyahi.append(f"<li><small style='color:#0057b7'>[{ad}]</small> <a href='{full_href}' target='_blank'>{item.text.strip()}</a></li>")
                        count += 1
        except:
            continue
            
    return yeni_siyahi

# 1. Köhnə xəbərləri oxu
kohne_xeberler = []
if os.path.exists("index.html"):
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
        kohne_xeberler = re.findall(r"<li>.*?</li>", content)

# 2. Yeni xəbərləri 3 fərqli saytdan çək
yeni_gelenler = xeberleri_getir()

# 3. Dublikatları təmizlə və birləşdir (Yenilər başda olsun)
# Siyahını bir az böyüdürük (məsələn, 200 xəbərə qədər)
butun_xeberler = yeni_gelenler + [x for x in kohne_xeberler if x not in yeni_gelenler]
butun_xeberler = butun_xeberler[:200]

# 4. Dizayn
indiki_vaxt = datetime.now().strftime("%d.%m.%Y %H:%M")
html_basliq = f"""
<!DOCTYPE html>
<html lang='az'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>Cuppulu News Portal</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 0; background: #0a0a0a; color: #e0e0e0; 
               background-image: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2070');
               background-size: cover; background-attachment: fixed; }}
        .container {{ max-width: 900px; margin: 40px auto; background: rgba(15,15,15,0.95); padding: 30px; border-radius: 25px; border: 1px solid #333; box-shadow: 0 10px 50px rgba(0,0,0,0.5); }}
        h1 {{ text-align: center; color: #fff; text-transform: uppercase; letter-spacing: 5px; border-bottom: 2px solid #0057b7; padding-bottom: 15px; margin-bottom: 30px; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: rgba(255,255,255,0.03); margin-bottom: 10px; padding: 15px; border-radius: 12px; transition: 0.2s; display: flex; align-items: center; gap: 10px; }}
        li:hover {{ background: rgba(0,87,183,0.1); transform: translateX(5px); }}
        a {{ text-decoration: none; color: #ddd; font-size: 17px; line-height: 1.4; }}
        a:hover {{ color: #0057b7; }}
        .footer {{ text-align: center; margin-top: 40px; color: #555; font-size: 13px; border-top: 1px solid #222; padding-top: 20px; }}
    </style>
</head>
<body>
    <div class='container'>
        <h1>CUPPULU NEWS</h1>
        <ul>
"""

html_sonluq = f"""
        </ul>
        <div class='footer'>
            <p>Sistem: 3 Mənbədən Avtomatik Yenilənmə | Son: {indiki_vaxt}</p>
        </div>
    </div>
</body>
</html>
"""

tam_html = html_basliq + "".join(butun_xeberler) + html_sonluq
with open("index.html", "w", encoding="utf-8") as f:
    f.write(tam_html)
print(f"Toplam {len(butun_xeberler)} xəbər yerləşdirildi.")
