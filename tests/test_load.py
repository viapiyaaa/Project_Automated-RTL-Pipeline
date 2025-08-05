import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

class TestLoadFunctions(unittest.TestCase):

    # Test untuk memastikan fungsi save_to_csv memanggil to_csv dengan benar
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_save_to_csv_writes_correctly(self, mock_to_csv):
        # Data dummy untuk pengujian
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [15000, 20000],
            'rating': [3.5, 4.0]
        })

        # Panggil fungsi yang akan diuji
        save_to_csv(df, 'test_output.csv')

        # Pastikan fungsi to_csv dipanggil dengan parameter yang tepat
        mock_to_csv.assert_called_once_with('test_output.csv', index=False)

    # Test untuk memastikan save_to_google_sheets memanggil Google Sheets API update
    @patch('utils.load.build')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets_calls_update_api(self, mock_creds, mock_build):
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [15000, 20000],
            'rating': [3.5, 4.0]
        })

        # Mock kredensial Google API
        mock_creds.return_value = MagicMock()
        mock_service = MagicMock()

        # Mock chaining method .spreadsheets().values().update().execute()
        mock_service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = None
        mock_build.return_value = mock_service

        # Jalankan fungsi
        save_to_google_sheets(df, 'dummy_spreadsheet_id', 'Sheet1!A2')

        # Pastikan update API dipanggil sekali
        mock_service.spreadsheets.return_value.values.return_value.update.assert_called_once()

    # Test untuk memastikan data dikirim ke PostgreSQL menggunakan to_sql
    @patch('utils.load.create_engine')
    def test_load_to_postgresql_executes_to_sql(self, mock_create_engine):
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [15000, 20000],
            'rating': [3.5, 4.0]
        })

        # Mock engine PostgreSQL
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine

        # Patch to_sql untuk memastikan dipanggil
        with patch('pandas.DataFrame.to_sql') as mock_to_sql:
            load_to_postgresql(df)
            mock_to_sql.assert_called_once()

    # Test untuk menangani error ketika gagal koneksi ke PostgreSQL
    @patch('utils.load.create_engine')
    def test_load_to_postgresql_connection_error(self, mock_create_engine):
        df = pd.DataFrame({
            'title': ['Product 1', 'Product 2'],
            'price': [15000, 20000],
            'rating': [3.5, 4.0]
        })

        # Simulasikan error saat membuat koneksi ke database
        mock_create_engine.side_effect = Exception("Database connection error")

        # Patch print untuk menangkap pesan error
        with patch('builtins.print') as mock_print:
            load_to_postgresql(df)
            mock_print.assert_any_call("Gagal menyimpan ke PostgreSQL: Database connection error")

# Menjalankan semua test jika file ini dijalankan langsung
if __name__ == '__main__':
    unittest.main()
