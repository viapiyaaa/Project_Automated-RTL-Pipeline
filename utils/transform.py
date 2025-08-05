import pandas as pd
import numpy as np
from datetime import datetime
import warnings

# Menonaktifkan peringatan FutureWarning dari pandas (terkait perubahan di versi mendatang)
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('future.no_silent_downcasting', True)

def transform_data(raw_products):
    """
    Melakukan transformasi data mentah produk fashion agar bersih dan siap dianalisis.

    Args:
        raw_products (list or dict): Data mentah hasil scraping atau input.

    Returns:
        pd.DataFrame: DataFrame yang telah dibersihkan dan ditransformasi.
    """
    # Konversi data mentah ke DataFrame
    df = pd.DataFrame(raw_products)
    
    # Filter data: Hapus produk yang memiliki judul 'unknown product' (tidak valid)
    df = df[df['title'].str.lower() != 'unknown product']
    
    # Bersihkan dan ubah kolom harga menjadi float (dalam satuan rupiah)
    df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).replace('', np.nan)  
    df.dropna(subset=['price'], inplace=True)  
    df['price'] = df['price'].astype(float) * 16000  
    
    # Bersihkan dan ubah kolom rating menjadi float
    df['rating'] = df['rating'].replace(r'[^0-9.]', '', regex=True).replace('', np.nan)  
    df.dropna(subset=['rating'], inplace=True)  
    df['rating'] = df['rating'].astype(float)
    
    # Bulatkan ke bawah ke 1 angka di belakang koma
    df['rating'] = np.floor(df['rating'] * 10) / 10
    
    # Ekstrak jumlah warna (angka) dari kolom colors
    df['colors'] = df['colors'].replace(r'\D', '', regex=True).replace('', np.nan)
    df.dropna(subset=['colors'], inplace=True)
    df['colors'] = df['colors'].astype(int)
    
    # Bersihkan kolom size dan ubah menjadi huruf kapital (S, M, L, dll)
    df['size'] = df['size'].replace(r'Size:\s*', '', regex=True).str.upper()
    
    # Bersihkan kolom gender dan kapitalisasi huruf pertamanya
    df['gender'] = df['gender'].replace(r'Gender:\s*', '', regex=True).str.capitalize()
    
    # Pastikan tipe data size dan gender adalah objek (string)
    df['size'] = df['size'].astype('object')
    df['gender'] = df['gender'].astype('object')

    # Hapus duplikasi dan baris yang masih memiliki nilai kosong
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)
    
    # Tambahkan kolom timestamp saat data diproses
    df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Urutkan kolom agar lebih rapi
    df = df[[ 'title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp' ]]
    
    return df
