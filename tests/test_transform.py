import unittest
from unittest.mock import patch
import pandas as pd
from utils.transform import transform_data

# Kelas untuk menguji fungsi transform_data
class TestTransformData(unittest.TestCase):

    # Setup awal: Menyediakan data dummy untuk beberapa kasus
    def setUp(self):
        # Data valid (semua nilai dapat dikonversi dengan benar)
        self.valid_products = [
            {'title': 'Product 1', 'price': '15000', 'rating': '3.5', 'colors': '3', 'size': 'M', 'gender': 'Women'},
            {'title': 'Product 2', 'price': '20000', 'rating': '4.0', 'colors': '3', 'size': 'L', 'gender': 'Men'}
        ]
        
        # Data dengan price tidak valid (string non-angka)
        self.invalid_price_products = [
            {'title': 'Product 3', 'price': 'invalid_price', 'rating': '3.0', 'colors': '2', 'size': 'S', 'gender': 'Men'}
        ]
        
        # Data dengan rating tidak valid (string non-angka)
        self.invalid_rating_products = [
            {'title': 'Product 4', 'price': '25000', 'rating': 'invalid_rating', 'colors': '1', 'size': 'XL', 'gender': 'Unisex'}
        ]

    # Uji transform_data dengan data valid
    def test_transform_data_success(self):
        df = transform_data(self.valid_products)
        
        # Pastikan jumlah baris sesuai data valid
        self.assertEqual(len(df), 2)
        
        # Pastikan kolom penting ada
        self.assertIn('price', df.columns)
        self.assertIn('rating', df.columns)
        self.assertIn('timestamp', df.columns)

        # Pastikan tipe data kolom price dan rating adalah numerik
        self.assertTrue(pd.api.types.is_numeric_dtype(df['price']), "Kolom price harus numerik")
        self.assertTrue(pd.api.types.is_numeric_dtype(df['rating']), "Kolom rating harus numerik")
        
        # Pastikan semua nilai price dan rating positif
        self.assertTrue((df['price'] > 0).all(), "Semua harga harus positif")
        self.assertTrue((df['rating'] > 0).all(), "Semua rating harus positif")

    # Uji jika harga tidak valid (tidak bisa dikonversi ke float)
    def test_transform_data_invalid_price(self):
        df = transform_data(self.invalid_price_products)
        
        # Seharusnya tidak ada data yang lolos
        self.assertEqual(len(df), 0)

    # Uji jika rating tidak valid
    def test_transform_data_invalid_rating(self):
        df = transform_data(self.invalid_rating_products)
        
        # Seharusnya tidak ada data yang lolos
        self.assertEqual(len(df), 0)

    # Uji jika terdapat data campuran antara valid dan tidak valid
    def test_transform_data_mixed_valid_invalid(self):
        mixed = self.valid_products + self.invalid_price_products + self.invalid_rating_products
        df = transform_data(mixed)
        
        # Hanya data valid yang seharusnya masuk ke DataFrame
        self.assertEqual(len(df), len(self.valid_products))


# Eksekusi semua unit test jika file dijalankan secara langsung
if __name__ == '__main__':
    unittest.main()
