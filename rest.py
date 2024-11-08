from flask import Flask
from flask_cors import CORS, cross_origin
from langchain.chat_models import ChatOpenAI
from langchain_community.document_loaders.csv_loader import CSVLoader
# from langchain.llms import OpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
import random
import time

# Start config value
app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

user = '리지엔씬'
des_user = 'My name is ' + user
OPENAI_API_KEY=''
chat = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model='gpt-3.5-turbo'
)
# Initial value
messages = []
source_knowledge = ''

loader = CSVLoader(file_path="./employee_data.csv")
data = loader.load_and_split()

with open('hr_policy.txt', 'r') as file:
   source_knowledge = file.read().replace('\n', '')

for m in data:
   source_knowledge += '\n' + m.page_content

source_knowledge += '\n' + des_user

augmented_prompt = f"""Using the contexts below, answer the query.

Contexts:
{source_knowledge}"""

prompt = HumanMessage(
   content=augmented_prompt
)
messages.append(prompt)

@app.get('/chat/<query>')
@cross_origin()
def chatting(query):
   prompt = HumanMessage(
      content='Query: ' + query
   )
   messages.append(prompt)
   res = chat(messages)
   messages.append(res)
   # res = response_generator(query)
   return {"chat": res.content}

# llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)

# Streamed response emulator
# def response_generator(query):
#    prompt = HumanMessage(
#       content=query
#    )
#    messages.append(prompt)
#    res = chat(messages)
#    messages.append(res)

#    return res.content