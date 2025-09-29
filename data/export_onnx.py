from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

model_id = "ProsusAI/finbert"
save_dir = "./finbert_onnx"

# Export ONNX model
model = ORTModelForSequenceClassification.from_pretrained(
    model_id,
    export=True
)
model.save_pretrained(save_dir)

# Save tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.save_pretrained(save_dir)
