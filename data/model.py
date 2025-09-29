# import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

class FinBERTModel:
    def __init__(self):
        self.pipe = pipeline("text-classification", model="ProsusAI/finbert")
        
        # Load model & tokenizer at startup
        # MODEL_NAME = "yiyanghkust/finbert-tone"
        # tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        # model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        # self.nlp_pipeline = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

    def predict(self, text):
        sentiment = self.pipe(text)[0]

        # sentiment = self.nlp_pipeline(text)[0]
        print(f'Sentiment: {sentiment["label"]} (Score: {sentiment["score"]:.4f})')

# Example usage
if __name__ == "__main__":
    finbert = FinBERTModel()
    sample_text = "The stock market is performing well."
    prediction = finbert.predict(sample_text)
    print(f"Prediction: {prediction}")