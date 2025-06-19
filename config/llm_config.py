llm_model = 'deepseek-r1:1.5b' # select any model available on the ollama site https://ollama.com/search

use_openai = False # set to True if using openai api and then select 'openai_model' variable. You need to add the openai api token in the .env file in the root dirextory

openai_model = 'gpt-4o' # if using openai api then select which model to use



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


record_data = True