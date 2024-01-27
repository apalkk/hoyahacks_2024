import dotenv
import openai
for k in dotenv.dotenv_values():
    openai.api_key=k


