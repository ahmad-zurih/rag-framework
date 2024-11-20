import ollama

class Responder:
    def __init__(self, data: str, model: str, prompt_template: str, query: str) -> None:
        self.data = data 
        self.model = model 
        self.prompt_template = prompt_template
        self.query = query

        self.prompt = prompt_template.format(data=self.data, query=self.query)

    
    def generate_response(self) -> str:
        try:
            model_output = ollama.generate(model=self.model, prompt=self.prompt)
            return model_output['response']
        except KeyError as e:
            raise ValueError(f"Response does not contain expected key: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")
