import unittest
from unittest.mock import patch, Mock

# Import fungsi scrape_main dari file utils/extract.py
from utils.extract import scrape_main

# HTML dummy sebagai data uji (mocked response) untuk mensimulasikan konten website
DUMMY_HTML = """
<html>
    <body>
        <div class="product-details">
            <h3 class="product-title">Sepatu Olahraga</h3>
            <span class="price">$207.02</span>
            <p>Rating: 4.5</p>
            <p>Merah, Hitam</p>
            <p>Ukuran: L</p>
            <p>Gender: Pria</p>
        </div>
        <div class="product-details">
            <h3 class="product-title">Kaos Santai</h3>
            <span class="price">$181.85</span>
            <p>Rating: 4.0</p>
            <p>Putih, Biru</p>
            <p>Ukuran: M</p>
            <p>Gender: Wanita</p>
        </div>
    </body>
</html>
"""

class TestScrapeMain(unittest.TestCase):
    @patch("utils.extract.requests.get")  
    def test_scrape_main_parsing(self, mock_get):
        # Buat objek mock response yang akan dikembalikan oleh requests.get
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = DUMMY_HTML.encode("utf-8")  
        mock_get.return_value = mock_response  

        # URL dummy karena request sebenarnya sudah dimock
        url = "http://dummyurl.com"
        result = scrape_main(url)

        # Pastikan jumlah produk yang diambil sesuai
        self.assertEqual(len(result), 2)

        # Cek parsing data untuk produk pertama
        self.assertEqual(result[0]["title"], "Sepatu Olahraga")
        self.assertEqual(result[0]["price"], "$207.02")
        self.assertEqual(result[0]["rating"], "4.5")
        self.assertEqual(result[0]["colors"], "Merah, Hitam")
        self.assertEqual(result[0]["size"], "L")
        self.assertEqual(result[0]["gender"], "Pria")

        # Cek parsing data untuk produk kedua
        self.assertEqual(result[1]["title"], "Kaos Santai")
        self.assertEqual(result[1]["price"], "$181.85")
        self.assertEqual(result[1]["rating"], "4.0")
        self.assertEqual(result[1]["colors"], "Putih, Biru")
        self.assertEqual(result[1]["size"], "M")
        self.assertEqual(result[1]["gender"], "Wanita")

# Menjalankan unit test jika file ini dijalankan langsung
if __name__ == "__main__":
    unittest.main()
