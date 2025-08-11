import requests
from bs4 import BeautifulSoup
from datetime import datetime

# URL sumber proxy (bisa ditambah lagi jika mau)
URL_LIST = [
    "https://www.sslproxies.org/",
    "https://free-proxy-list.net/",
    "https://www.us-proxy.org/"
]

def ambil_proxy_dari_url(url):
    print(f"[INFO] Mengambil proxy dari {url}")
    proxy_list = []
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", {"id": "proxylisttable"})
        if table:
            for row in table.tbody.find_all("tr"):
                cols = row.find_all("td")
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                country = cols[3].text.strip().lower()
                # Filter hanya proxy Indonesia
                if "indonesia" in country:
                    proxy_list.append(f"{ip}:{port}")
    except Exception as e:
        print(f"[ERROR] Gagal ambil dari {url}: {e}")
    return proxy_list

def cek_proxy(proxy):
    try:
        # Cek koneksi menggunakan HTTPS
        response = requests.get(
            "https://httpbin.org/ip",
            proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
            timeout=5
        )
        if response.status_code == 200:
            print(f"[AKTIF] {proxy}")
            return True
    except:
        pass
    return False

if __name__ == "__main__":
    semua_proxy = []
    for url in URL_LIST:
        semua_proxy.extend(ambil_proxy_dari_url(url))

    semua_proxy = list(set(semua_proxy))  # Hilangkan duplikat
    print(f"[INFO] Total proxy Indonesia ditemukan: {len(semua_proxy)}")

    aktif = []
    for proxy in semua_proxy:
        if cek_proxy(proxy):
            aktif.append(proxy)

    print(f"[INFO] Total proxy aktif: {len(aktif)}")

    # Simpan dengan nama file format tanggal-jam
    filename = f"proxy-{datetime.now().strftime('%Y-%m-%d-%H-%M')}.txt"
    with open(filename, "w") as f:
        f.write("\n".join(aktif))

    print(f"[SELESAI] Proxy aktif disimpan di {filename}")
