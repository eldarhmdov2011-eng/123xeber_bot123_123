import requests
from bs4 import BeautifulSoup

def xeberleri_getir():
    url = "https://oxu.az"
    headers = {"User-Agent": "Mozilla/5.0"} # Sayta insan kimi görünmək üçün
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        xeberler = []
        # Oxu.az üçün xəbər başlıqlarını tapırıq
        for link in soup.find_all("a", class_="news-i-inner")[:10]:
            title = link.find("div", class_="title").text.strip()
            href = "https://oxu.az" + link.get("href")
            xeberler.append(f"<li><a href='{href}' target='_blank'>{title}</a></li>")
            
        return "".join(xeberler)
    except Exception as e:
        return f"<li>Xəbər tapılmadı: {e}</li>"

# HTML faylını yeniləyirik
yeni_xeberler = xeberleri_getir()
html_kod = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='UTF-8'>
    <title>Cuppulu Xəbər Portalı</title>
    <style>
        body {{ font-family: Arial; padding: 20px; background: #f4f4f4; }}
        h1 {{ color: #333; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ background: white; margin-bottom: 10px; padding: 15px; border-radius: 5px; }}
        a {{ text-decoration: none; color: blue; font-weight: bold; }}
    </style>
</head>
<body>
    <h1>Son Xəbərlər (Avtomatik Yenilənir)</h1>
    <ul>
        {yeni_xeberler}
    </ul>
    <p>Son yenilənmə: GitHub Actions tərəfindən</p>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_kod)

print("İş tamamlandı, xəbərlər yazıldı!")
