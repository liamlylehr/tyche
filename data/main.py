"""
this class will serve as the main entry point for the daily data ingestion and processing
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline
from google_news_scraper import GoogleNewsScraper

model = None

def app_lifespan(app: FastAPI):
    global model
    model = pipeline("sentiment-analysis", model="ProsusAI/finbert")
    print("Model loaded successfully.")

    yield
    print("Application shutting down.")

app = FastAPI(lifespan=app_lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Replace with specific origins for better security.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --------------------------------

class SearchRequest(BaseModel):
    company_name: str
    limit: int = 5

@app.post("/search_sentiments")
async def search_company_sentiments(request: SearchRequest):
    """Endpoint to search news articles and analyze sentiments"""
    global model
    if model is None:
        return {"message": "Model not loaded. Please check the application startup logs."}
    
    scraper = GoogleNewsScraper(request.company_name)
    scraper.parse_articles(request.limit)
    scraper.fetch_all_articles_content()
    
    # Perform sentiment analysis
    sentiments = [{"title": article.title, "sentiment": model.predict(article.title)} for article in scraper.articles]
    
    return {
        "query": request.company_name,
        "sentiments": sentiments
    }


@app.post("/search")
async def search_company_news(request: SearchRequest):
    """Endpoint to search news articles"""
    scraper = GoogleNewsScraper(request.company_name)
    scraper.parse_articles(request.limit)
    scraper.fetch_all_articles_content()
    
    return {
        "query": request.company_name,
        "articles": [
            {
                "title": article.title,
                "link": article.link,
                "date": article.date,
                "content": article.content
            } for article in scraper.articles
        ]
    }

