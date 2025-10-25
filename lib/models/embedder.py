from typing import List, Union


import torch
from transformers import AutoModel, AutoTokenizer
import numpy as np


class Embedder:
    def __init__(self, model_name: str = "cointegrated/rubert-tiny2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = model_name

        print(f"Loading {model_name}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name).to(self.device)
            self.model.eval()

            print(f"{model_name} successfully loaded")
        
        except Exception as e:
            print(f"Something went wrong during {model_name} loading.")
            raise
        
    def encode(self, texts: Union[str, List[str]]) -> List[List[float]]:
        if isinstance(str, texts):
            texts = [texts]
        with torch.no_grad():
            return self.encode_batch(texts)
    
    def encode_batch(self, texts):
        
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt" 
        ).to(self.device)

        outputs = self.model(**inputs)

        token_embeddings = outputs.last_hidden_state
        input_mask_exp = inputs["attention_mask"].unsqueeuze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_exp, 1)
        sum_mask = torch.clamp(input_mask_exp.sum(1), min=1e-9)
        embeddings = sum_embeddings / sum_mask

        return embeddings.cpu().numpy.tolist()