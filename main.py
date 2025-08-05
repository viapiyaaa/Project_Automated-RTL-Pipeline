import logging
from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, load_to_postgresql

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("fashion_scraper_etl.log"),
        logging.StreamHandler()
    ]
)

def scrape_all_pages(base_url: str, total_pages: int = 50) -> list:
    """Scrape produk dari halaman 1 hingga halaman terakhir."""
    all_products = []
    for page in range(1, total_pages + 1):
        url = base_url if page == 1 else f"{base_url}page{page}"
        logging.info(f"Scraping dari URL: {url}")
        try:
            products = scrape_main(url)
            all_products.extend(products)
        except Exception as e:
            logging.error(f"Gagal scraping halaman ke-{page}: {e}")
    return all_products

def etl_pipeline():
    base_url = 'https://fashion-studio.dicoding.dev/'
    
    logging.info("Memulai proses ETL Fashion Product Scraper")

    # Extract
    raw_data = scrape_all_pages(base_url)

    # Transform
    transformed_data = transform_data(raw_data)
    logging.info("Transformasi data selesai")

    # Load 
    save_to_csv(transformed_data)
    logging.info("Data disimpan dalam format CSV")

    load_to_postgresql(transformed_data)
    logging.info("Data dimuat ke PostgreSQL")

    save_to_google_sheets(
        transformed_data,
        sheet_id='10LI3mgtay9vtvU9mGCOzJxny-pTVUxawUiwaRlxBi6c',
        range_name='SHEET1!A1'
    )
    logging.info("Data berhasil disimpan ke Google Sheets")

    logging.info("Proses ETL selesai")

if __name__ == '__main__':
    etl_pipeline()
