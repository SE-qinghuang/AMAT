from transformers import AutoTokenizer, AutoModelForMaskedLM
tokenizer = AutoTokenizer.from_pretrained("ZQ/Type_Inference")
model = AutoModelForMaskedLM.from_pretrained("ZQ/Type_Inference")