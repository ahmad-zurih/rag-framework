import ollama


class Responder:
    def __init__(self, data: str, model: str, prompt_template: str, query: str) -> None:
        self.data = data 
        self.model = model 
        self.prompt_template = prompt_template
        self.query = query

        self.prompt = prompt_template.format(data=self.data, query=self.query)

    
    def generate_response(self) -> str:
        self._check_model()
        try:
            model_output = ollama.generate(model=self.model, prompt=self.prompt)
            return model_output['response']
        except KeyError as e:
            raise ValueError(f"Response does not contain expected key: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")
        
    def _check_model(self):
        try:
            models = ollama.list()['models']
            model_names = [model['name'] for model in models]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve the list of models: {e}")

        if self.model not in model_names:
            print(f"Model '{self.model}' is not downloaded. Attempting to download...")
            try:
                ollama.pull(self.model)
                print(f"Successfully downloaded model '{self.model}'.")
            except ollama._types.ResponseError as e:
                raise ValueError(f"Model '{self.model}' does not exist in the Ollama repository. Please check the model name.")
            except Exception as e:
                raise RuntimeError(f"An error occurred while downloading the model '{self.model}': {e}")
