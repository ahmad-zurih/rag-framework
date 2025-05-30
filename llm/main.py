import ollama
import openai


class Responder:
    """
    A class to generate responses using the Ollama LLM within a RAG framework.
    """

    def __init__(self, data: str, model: str, prompt_template: str, query: str) -> None:
        """
        Initialize the Responder instance.

        Args:
            data: The output from the retriever to be added to the prompt
            model: The name of the LLM model to use.
            prompt_template: The template string for the prompt.
            query: The user's query.
        """
        self.data = data 
        self.model = model 
        self.prompt_template = prompt_template
        self.query = query

        self.prompt = prompt_template.format(data=self.data, query=self.query)

    
    def generate_response(self) -> str:
        """
        Generate a response based on the query and data.

        Returns:
            The response generated by the LLM.
        """
        self._check_model()
        try:
            model_output = ollama.generate(model=self.model, prompt=self.prompt)
            return model_output['response']
        except KeyError as e:
            raise ValueError(f"Response does not contain expected key: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")
        

    def stream_response(self):
        """
        Stream a response based on the query and data for a chatbot environment.
        """
        self._check_model()
        try:
            response_generator = ollama.generate(model=self.model, prompt=self.prompt, stream=True)
            
            for chunk in response_generator:
                print(chunk['response'], end='', flush=True)
            print("\n")
            return ""

        except KeyError as e:
            raise ValueError(f"Response does not contain expected key: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")
        
    
    def stream_response_chunks(self):
        """
        Returns a generator that yields chunks of the response text.
        """
        self._check_model()
        try:
            response_generator = ollama.generate(model=self.model, prompt=self.prompt, stream=True)
            for chunk in response_generator:
                yield chunk['response']
        except KeyError as e:
            raise ValueError(f"Response does not contain expected key: {e}")
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")

        
    def _check_model(self):
        """
        Herper function to check if the specified model is available. If not, attempt to download it.
        """
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
            except ollama.ResponseError as e:
                raise ValueError(f"Model '{self.model}' does not exist in the Ollama repository. Please check the model name.")
            except Exception as e:
                raise RuntimeError(f"An error occurred while downloading the model '{self.model}': {e}")


class OpenAIResponder:
    """
    A class to generate responses using the OpenAI API within a RAG framework.
    """

    def __init__(self, data: str, model: str, prompt_template: str, query: str, cleint: openai.OpenAI) -> None:
        """
        Initialize the OpenAIResponder instance.

        Args:
            data: The output from the retriever to be added to the prompt.
            model: The name of the OpenAI model to use (e.g., 'gpt-3.5-turbo').
            prompt_template: The template string for the prompt.
            query: The user's query.
        """
        self.data = data
        self.model = model
        self.prompt_template = prompt_template
        self.query = query
        self.cleint = cleint
        
        # Construct the final prompt
        self.prompt = prompt_template.format(data=self.data, query=self.query)

    def generate_response(self) -> str:
        """
        Generate a response based on the query and data.

        Returns:
            The response generated by the OpenAI model.
        """
        try:
            # For ChatCompletion API
            response = self.cleint.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a RAG system."},
                    {"role": "user", "content": self.prompt},
                ],
                max_tokens=1024,
                temperature=0.7,
                stream=False,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"An error occurred during response generation: {e}")

    def stream_response(self):
        """
        Stream a response based on the query and data for a chatbot environment.
        Prints chunks to stdout as they arrive.
        """
        try:
            response_stream = self.cleint.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a RAG system."},
                    {"role": "user", "content": self.prompt},
                ],
                max_tokens=1024,
                temperature=0.7,
                stream=True,
            )
            for chunk in response_stream:
                # 'delta' contains the incremental text
                chunk_text = chunk.choices[0].delta.content or ""
                print(chunk_text, end='', flush=True)
            print("\n")
            return ""
        except Exception as e:
            raise RuntimeError(f"An error occurred during response streaming: {e}")

    def stream_response_chunks(self):
        """
        Returns a generator that yields chunks of the response text.
        """
        try:
            response_stream = self.cleint.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a RAG system."},
                    {"role": "user", "content": self.prompt},
                ],
                max_tokens=1024,
                temperature=0.7,
                stream=True,
            )
            for chunk in response_stream:
                chunk_text = chunk.choices[0].delta.content or ""
                yield chunk_text
        except Exception as e:
            raise RuntimeError(f"An error occurred during chunk-based response streaming: {e}")