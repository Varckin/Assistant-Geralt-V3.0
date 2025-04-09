from llama_cpp import Llama
from pathlib import Path

class NLP:
    def __init__(self):
        self.model = Llama(
            model_path=str(Path('NLP/model/mistral-7b-instruct-v0.1.Q4_K_M.gguf')),
            n_ctx=4096,
            n_threads=6,
            use_mlock=True
        )

    async def generation(self, prompt: str) -> str:
        response = self.model(prompt, max_tokens=1028, temperature=0.7, top_p=0.95)
        return response["choices"][0]["text"].strip()
