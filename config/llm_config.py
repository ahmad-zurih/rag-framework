llm_model = 'llama3.1:8b' # select any model available on the ollama site https://ollama.com/search

use_openai = False # set to True if using openai api and then select 'openai_model' variable

openai_model = 'gpt-4o' # if using openai api then select which model to use




#prompt = """
#You are a helpful polite assistat that works at the Data Science Lab (DSL). given the following data about DSL: \n {data} \n
#and the following query: \n{query}\n
#generate a responde. If there are no relevant information in the data, state that you don't have  relevant information
#"""
prompt = """
DOCUMENTS: \n
{data}
\n
\n
QUESTION:
{query}
\n
\n
INSTRUCTIONS:
Answer the users QUESTION using the DOCUMENTS text above.
Keep your answer ground in the facts of the DOCUMENT.
If the DOCUMENT doesn’t contain the facts to answer the QUESTION return NO Answer found
"""