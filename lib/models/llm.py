from vllm import LLM, SamplingParams
from typing import List, Optional

class LLMTest:
    def __init__(self, model_name: str = "some_name"):
        pass

        print(f"loading {model_name}")

        self.model_name = model_name

        llm = LLM(model=model_name, tensor_parallel_size=1, gpu_memory_utilization=0.8, max_model_len = 1024)
        self.sampling_params = SamplingParams(temperature=0.9, top_p=0.9, max_tokens=512, stop=['<\s>', '###'])

        print(f"success!")

    
    def generate(self, promt: str, **kwargs) -> str:
        outputs = self.llm.generate([promt], self.sampling_params)

        return outputs[0].outputs[0].text.strip()

    def rag_generate(self, promt: str, context: str) -> str:
        return f"Используй контекст, чтобы ответить на вопрос, если в контексте нет информации для ответа, \
        скажи об этом. \
        Контекст: {context} \
        Вопрос: {promt}"
