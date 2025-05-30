from llama_cpp import Llama

class LLaMAChat:
    def __init__(self, model_path):
        self.model = Llama(model_path=model_path)
    
    def chat(self, message):
        if not self.model:
            return "⚠️ Model not loaded."
        response = self.model(f"### Human: {message}\n### Assistant:", max_tokens=200)
        return response["choices"][0]["text"].strip()
