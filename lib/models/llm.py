import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, GenerationConfig, AutoModelForCausalLM

class LLMTest:
    def __init__(self, model_name: str ="KingNish/Reasoning-0.5b"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"loading {model_name}")
        print(self.device)
        self.model_name = model_name

        # Загрузка токенизатора и модели
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )
        
        # Для моделей Qwen нужно установить pad_token
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True
        )
        
        # Параметры генерации, соответствующие оригинальному коду
        self.generation_config = GenerationConfig(
            temperature=0.7,
            top_p=0.9,
            max_new_tokens=512,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.1)

        print(f"success!")

    def generate(self, prompt: str, **kwargs) -> str:
        # Токенизация с учетом формата Qwen
        inputs = self.tokenizer(
            prompt, 
            return_tensors="pt", 
            padding=True, 
            truncation=True,
            max_length=1024
        ).to(self.device)
        
        # Генерация
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config,
                **kwargs
            )
        
        # Декодирование и удаление промта из результата
        generated_text = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:], 
            skip_special_tokens=True
        )
        
        return generated_text.strip()

    def rag_generate(self, prompt: str, context: str) -> str:
        # Форматирование промта для RAG
        formatted_prompt = f"""
Ты — помощник, который отвечает только на основе приведённого контекста.
Если в контексте нет достаточных данных, прямо сообщи об этом и не выдумывай.

Контекст:
{context}

Вопрос:
{prompt}

Дай развёрнутый ответ, опираясь исключительно на контекст:
"""

        return formatted_prompt

































































































# from transformers import AutoTokenizer, AutoModelForCausalLM
# import torch
# class LLMTest:
#     def __init__(self, model_name: str = "haiFrHust/VNJPTranslate_base"):
#         self.device = "cuda" if torch.cuda.is_available() else "cpu"
#         print(f"loading {model_name}")

#         self.model_name = model_name

#         # self.llm = LLM(model=model_name, tensor_parallel_size=1, gpu_memory_utilization=0.8, max_model_len = 1024)
#         # self.sampling_params = SamplingParams(temperature=0.9, top_p=0.9, max_tokens=512, stop=[r'<\s>', '###'])
#         self.tokenizer = AutoTokenizer.from_pretrained(model_name)
#         self.model = AutoModelForCausalLM.from_pretrained(
#             model_name,
#             torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
#             device_map="auto" if self.device == "cuda" else None,
#             trust_remote_code=True
#         )
        
#         self.sampling_params = {
#         "temperature": 0.9,
#         "top_p": 0.9, 
#         "max_new_tokens": 512,
#         "do_sample": True,
#         "pad_token_id": self.tokenizer.eos_token_id,
#         "eos_token_id": self.tokenizer.eos_token_id,
#             }

#         print(f"success!")

    
#     def generate(self, promt: str, **kwargs) -> str:
#         outputs = self.llm.generate([promt], self.sampling_params)

#         return outputs[0].outputs[0].text.strip()

#     def rag_generate(self, promt: str, context: str) -> str:
#         return f"Используй контекст, чтобы ответить на вопрос, если в контексте нет информации для ответа, \
#         скажи об этом. \
#         Контекст: {context} \
#         Вопрос: {promt}"
