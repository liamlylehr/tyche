import requests
from bs4 import BeautifulSoup
from beat_captcha import CaptchaBypasser
    
class Article:
    def __init__(self, title: str, link: str, date: str, link1: str = None, content: str = None):
        self.title = title
        self.link = link
        self.link1 = None
        self.date = date
        self.content = None

    def __repr__(self):
        # if self.content:
        #     return f"Article(title={self.title}, link={self.link}, date={self.date}, content={self.content})"
        if self.link1:
            return f"Article(title={self.title}, link={self.link}, date={self.date}, link1={self.link1})"
        return f"Article(title={self.title}, link={self.link}, date={self.date})"
    
class GoogleNewsScraper:
    def __init__(self, query: str):
        self.query = query
        self.gl = 'us'
        self.hl = 'en'
        # Construct the Google News search URL (query needs to be URL-encoded, %20 for whitespace)
        self.url = f'https://news.google.com/search?q={self.query}&hl={self.hl}-US&gl={self.gl}&ceid=US%3Aen'

        self.soup = None

        # Redirect URL for Google News, which is used to fetch the latest articles
        # self.redirect_url = 'https://news.google.com/read/CBMihgFBVV95cUxQUFFHUHVvak5faW82TFpSMFlwWk8yY1dOaXdLTGl4dnBLUU04YXhlRE5mLW43WWQ3Unl4SzhfYXQyMjkyc29tckFPM2E4UzdUeUJhVFQ5ZGJHVGdadHNzenZ4dTJiaUNzcmpYU0JuZU9VUlByTnlGTWRFVjYyN1BLeDc5SXJ5QQ?hl=en-US&gl=US&ceid=US%3Aen'
        
        self.articles = []  # Initialize an empty list to store articles

    def fetch_page(self):
        """Fetch the Google News page and return BeautifulSoup object"""
        try:
            response = requests.get(self.url)
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
    
    # Parse articles from the fetched page, articles_limit limits the number of articles to parse
    # articles_limit defaults to 100, needs to be less than or equal to 100 (TODO add a check later)
    def parse_articles(self, articles_limit: int = 100):
        """Parse articles from the fetched page"""
        self.soup = self.fetch_page()

        if not self.soup:
            print("No soup object to parse.")
            return
        
        # Find all article elements
        article_elements = self.soup.find_all('article')
        
        for article in article_elements[:articles_limit]:
            # print(article)
            link_element, title_element = article.find_all('a', href=True)

            date_element = article.find('time')

            title = self.clean_text(title_element.get_text()) if title_element else "No Title"
            link = link_element['href'] if link_element else "No Link"
            date = date_element['datetime'] if date_element else "No Date"

            link = f"https://news.google.com{link}" if link.startswith('./') else link

            link1 = CaptchaBypasser.get_final_url_selenium(link)
            
            # Create an Article object and append to the articles list
            article_obj = Article(title, link, date, link1)
            self.articles.append(article_obj)

    def fetch_article_content(self, article: Article):
        """Fetch the full content of a given article"""
        try:
            response = requests.get(article.link)
            response.raise_for_status()
            article_soup = BeautifulSoup(response.content, 'html.parser')
            paragraphs = article_soup.find_all('p')
            content = "\n".join([self.clean_text(p.get_text()) for p in paragraphs])
            article.content = content
            print(content)
        except requests.RequestException as e:
            print(f"Error fetching article content: {e}")
            article.content = "Content could not be fetched."

    def fetch_all_articles_content(self):
        """Fetch content for all articles"""
        for article in self.articles:
            self.fetch_article_content(article)

if __name__ == "__main__":
    query = "citibank"
    scraper = GoogleNewsScraper(query)
    scraper.parse_articles(1)
    scraper.fetch_all_articles_content()

    print(f"Found {len(scraper.articles)} articles for query '{query}':")
    for article in scraper.articles:
        print("\n", article)