import requests
from bs4 import BeautifulSoup

# Header untuk menyamarkan permintaan agar dianggap seperti browser biasa
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

# Fungsi utama untuk melakukan web scraping
def scrape_main(url):
    try:
        # Kirim permintaan HTTP GET ke URL yang ditentukan
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  
    except requests.exceptions.RequestException:
        # Jika gagal koneksi atau error HTTP lainnya
        raise Exception("Failed to access URL")

    # Parsing konten HTML menggunakan BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Cari semua elemen div dengan class "product-details"
    product_sections = soup.find_all("div", class_="product-details")

    # Jika tidak ditemukan, anggap parsing gagal
    if not product_sections:
        raise Exception("Failed to parse HTML")

    # List penampung data produk
    data = []

    # Iterasi setiap section produk
    for section in product_sections:
        try:
            # Ambil elemen-elemen yang berisi data produk
            title_tag = section.find("h3", class_="product-title")
            price_tag = section.find("span", class_="price")
            p_tags = section.find_all("p")  # Biasanya berisi rating, warna, ukuran, dll.

            # Default nilai jika tidak ditemukan
            title = title_tag.text.strip() if title_tag else "N/A"
            price = price_tag.text.strip() if price_tag else "N/A"
            rating = colors = size = gender = "N/A"

            # Loop untuk membaca isi setiap <p>
            for p in p_tags:
                text = p.text.strip()
                lower_text = text.lower()

                # Deteksi berdasarkan kata kunci
                if "rating:" in lower_text:
                    rating = text.split(":", 1)[1].strip()
                elif "ukuran" in lower_text or "size" in lower_text:
                    size = text.split(":", 1)[1].strip() if ":" in text else text
                elif "gender:" in lower_text:
                    gender = text.split(":", 1)[1].strip()
                elif ":" not in text:
                    # Diasumsikan sebagai informasi warna jika tidak ada titik dua
                    colors = text

            # Tambahkan data yang telah diambil ke dalam list
            data.append({
                "title": title,
                "price": price,
                "rating": rating,
                "colors": colors,
                "size": size,
                "gender": gender
            })

        except Exception as e:
            print(f"Error parsing section: {e}")
            continue  

    return data 
