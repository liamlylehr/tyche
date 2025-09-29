from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CaptchaBypasser:
    def get_final_url_selenium(url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Remove this to see the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        # Optional: Use undetected-chromedriver to avoid detection
        # from undetected_chromedriver import Chrome
        # driver = Chrome(options=chrome_options)
        
        driver = webdriver.Chrome(options=chrome_options)
        
        try:
            driver.get(url)
            
            # Wait for potential redirects to complete
            WebDriverWait(driver, 10).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            
            final_url = driver.current_url
            return final_url
            
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            driver.quit()