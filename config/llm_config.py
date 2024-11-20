llm_model = 'qwen2.5-coder:1.5b' # select any model available on the ollama site https://ollama.com/search


prompt = """
given the following data: {data}
and the following query: {query}
generate a responde. If there are no relevant information in the data, state that you don't have an answer
"""