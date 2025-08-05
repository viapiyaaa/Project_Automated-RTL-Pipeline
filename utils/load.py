import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from sqlalchemy import create_engine

def save_to_csv(df, filename="products.csv"):
    """
    Simpan DataFrame ke file CSV lokal.
    
    Args:
        df (pd.DataFrame): Data yang akan disimpan.
        filename (str): Nama file CSV ("products.csv").
    """
    df.to_csv(filename, index=False)
    print(f"Data berhasil disimpan ke file CSV: {filename}")


def save_to_google_sheets(df, sheet_id, range_name):
    """
    Simpan DataFrame ke Google Sheets.
    
    Args:
        df (pd.DataFrame): Data yang akan dikirim.
        sheet_id (str): ID dari Google Spreadsheet.
        range_name (str): Nama sheet dan range (contoh: 'Sheet1!A1').
    """
    # Autentikasi menggunakan credentials dari file JSON
    creds = Credentials.from_service_account_file('client_secret.json')
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Konversi DataFrame ke list 2D (termasuk header)
    values = [df.columns.tolist()] + df.values.tolist()
    body = {'values': values}

    # Kirim data ke Google Sheets
    sheet.values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"Data berhasil dikirim ke Google Sheets (range: {range_name}).")


def load_to_postgresql(df, table_name='products'):
    """
    Simpan DataFrame ke tabel PostgreSQL.
    
    Args:
        df (pd.DataFrame): Data yang akan disimpan.
        table_name (str): Nama tabel di PostgreSQL ('products').
    """
    try:
        # Detail koneksi ke PostgreSQL
        username = 'eviafiyatus'
        password = 'evi123'
        host = 'localhost'
        port = '5432'
        database = 'fashion'

        # Buat engine SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

        # Simpan ke PostgreSQL (replace: ganti tabel jika sudah ada)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke PostgreSQL dalam tabel '{table_name}'.")

    except Exception as e:
        print(f"Gagal menyimpan ke PostgreSQL: {e}")
