# Tyche - Data Pipeline

Managing data ingestion and processing

## Schemas

### companies

The companies schema hosts tables related to general company information

sp500_companies - Table containing general information regarding the companies listed in the sp500 index

| Column Name    | Data Type   | Description                  |
| -------------- | ----------- | ---------------------------- |
| id             | SERIAL      | Primary key                  |
| ticker         | VARCHAR(5)  | Stock ticker symbol          |
| company_name   | TEXT        | Name of the company          |
| gcis_sector    | TEXT        | Sector classification        |
| gcis_subsector | TEXT        | Subsector classification     |
| hq_location    | TEXT        | Headquarters location        |
| date_added     | TEXT        | Date added to the S&P 500    |
| cik            | VARCHAR(10) | Central Index Key            |
| year_founded   | TEXT        | Year the company was founded |

### media

Data related to collected media regarding entities with sentiment analysis results
Tables:

- media_clips - (need to review name and what data goes here)

## Files

### sp500_scraper.py

The Sp500WikipediaScraper class provides capability to scrape the Wikipedia page for the SP500 (https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) to collect general information on the companies.<br>
--> Aim of this is to then use the name and ticker to scrape media sources
