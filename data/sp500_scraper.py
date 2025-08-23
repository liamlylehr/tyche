import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List, Dict, Optional
from database_connection import DatabaseConnection

# Define a class to represent a singular company
class Company:
    def __init__(self, ticker: str, name: str, gcis_sector: str, gcis_subsector: str, hq_location: Optional[str], date_added: str, cik: str, year_founded: str):
        self.ticker = ticker
        self.name = name
        self.gcis_sector = gcis_sector
        self.gcis_subsector = gcis_subsector
        self.hq_location = hq_location
        self.date_added = date_added
        self.cik = cik
        self.year_founded = year_founded
    
    def __repr__(self):
        return (f"Company(ticker={self.ticker}, name={self.name}, "
                f"gcis_sector={self.gcis_sector}, gcis_subsector={self.gcis_subsector}, "
                f"hq_location={self.hq_location}, date_added={self.date_added}, "
                f"cik={self.cik}, year_founded={self.year_founded})")

# Class to bundle functionality for scraping S&P 500 data from Wikipedia
class sp500_wikipedia_scraper:
    def __init__(self):
        self.base_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        self.companies = []  # Initialize an empty list to store company data
        
    def fetch_page(self) -> Optional[BeautifulSoup]:
        """Fetch the S&P 500 page and return BeautifulSoup object"""
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching page: {e}")
            return None
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text data"""
        if not text:
            return ""
        return text.strip().replace('\n', '').replace('\t', '')
       
    def save_to_pg(self):
        """Save scraped data to postgres database"""
        db_conn = DatabaseConnection()

        with db_conn.get_connection() as conn:
            cur = conn.cursor()

            # Clear existing data in the table
            cur.execute("DELETE FROM companies.sp500_companies;")
            # Create table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies.sp500_companies (
                    id SERIAL PRIMARY KEY,
                    ticker VARCHAR(5),
                    company_name TEXT,
                    gcis_sector TEXT,
                    gcis_subsector TEXT,
                    hq_location TEXT,
                    date_added TEXT,
                    cik VARCHAR(10),
                    year_founded TEXT
                );
            """)
            
            # Insert each company into the database
            for company in self.companies:
                cur.execute("""
                    INSERT INTO companies.sp500_companies (ticker, company_name, gcis_sector, gcis_subsector, hq_location, date_added, cik, year_founded)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    company.ticker,
                    company.name,
                    company.gcis_sector,
                    company.gcis_subsector,
                    company.hq_location,
                    company.date_added,
                    company.cik,
                    company.year_founded
                ))
            conn.commit()
            
            # Fetch and print the saved data to verify
            cur.execute("SELECT * FROM companies.sp500_companies;")
            sp500 = cur.fetchall()
            print(sp500)
            print(f"Saved {len(self.companies)} companies to the database")


    def scrape_sp500_data(self) -> List[Company]:
        """Scrape all S&P 500 company data"""
        soup = self.fetch_page()
        if not soup:
            return []
        
        # Maintain a list to store company data
        self.companies = []
        
        # Find the main table with S&P 500 data
        table = soup.find('table')
        if not table:
            print("Could not find the main data table")
            return []
        
        # Find all table rows (skip header)
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            
            # Collect data from each cell, clean it and create a company object
            ticker = self.clean_text(cells[0].text)
            name = self.clean_text(cells[1].text)
            gcis_sector = self.clean_text(cells[2].text)
            gcis_subsector = self.clean_text(cells[3].text)
            hq_location = self.clean_text(cells[4].text)
            date_added = self.clean_text(cells[5].text)
            cik = self.clean_text(cells[6].text)
            year_founded = self.clean_text(cells[7].text)
            company_data = Company(ticker, name, gcis_sector, gcis_subsector, hq_location, date_added, cik, year_founded)
            
            self.companies.append(company_data)
        return self.companies
    

if __name__ == "__main__":
    scraper = sp500_wikipedia_scraper()
    companies = scraper.scrape_sp500_data()
        
    print(f"Scraped {len(companies)} companies from S&P 500")

    scraper.save_to_pg()
