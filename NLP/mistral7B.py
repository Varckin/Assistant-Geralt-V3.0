from llama_cpp import Llama
from pathlib import Path
import os

class NLP:
    def __init__(self):
        self.model = Llama(
            model_path=str(Path(os.getenv('NLP_PATH'))),
            n_ctx=4096,
            n_threads=6,
            use_mlock=True
        )

    async def generation(self, prompt: str) -> str:
        response = self.model(prompt, max_tokens=1028, temperature=0.7, top_p=0.95)
        return response["choices"][0]["text"].strip()
