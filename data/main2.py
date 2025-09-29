from fastapi import FastAPI
from pydantic import BaseModel
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, pipeline

app = FastAPI()
pipe = None

class TextInput(BaseModel):
    text: str

@app.on_event("startup")
def load_model():
    global pipe
    save_dir = "./finbert_onnx"
    model = ORTModelForSequenceClassification.from_pretrained(save_dir)
    tokenizer = AutoTokenizer.from_pretrained(save_dir)
    pipe = pipeline("text-classification", model=model, tokenizer=tokenizer)

@app.post("/predict")
def predict(input: TextInput):
    result = pipe(input.text)
    return {"label": result[0]["label"], "score": result[0]["score"]}
