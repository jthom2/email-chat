from langchain.llms import OpenAI
from langchain.agents.agent_toolkits import GmailToolkit
from langchain.chat_models import ChatOpenAI
from langchain.chat_loaders.gmail import GMailLoader
from langchain.tools.gmail.utils import build_resource_service, get_gmail_credentials
from langchain.agents import initialize_agent, AgentType
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_loaders.utils import (
    map_ai_messages,
)
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from decouple import config
from models import CreateDraftSchema, GenerateInput
import os
import os.path
import base64
import json
import re
import time
import logging
import requests

os.environ["OPENAI_API_KEY"] = config("OPENAI_API_KEY")

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

llm = ChatOpenAI(temperature=0.9, model="gpt-3.5-turbo-16k", max_retries=1)
gmail = GmailToolkit()

chain = load_qa_chain(llm, chain_type="map_reduce")

creds = None

if os.path.exists("email_token.json"):
    creds = Credentials.from_authorized_user_file("email_token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            SCOPES,
        )
        creds = flow.run_local_server(port=0)
    with open("email_token.json", "w") as token:
        token.write(creds.to_json())


loader = GMailLoader(creds=creds, n=3)
data = loader.load()
len(data)

training_data = list(map_ai_messages(data, sender="me"))


tools = GmailToolkit.get_tools(self=gmail)


agent = initialize_agent(
    tools=tools,
    llm=llm,
    chain=chain,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)






from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.post("/generate")
async def generate(prompt: GenerateInput):
    refined_prompt = f"""
    You are using my Gmail account: 
    prompt: {prompt.prompt}
    if create_gmail_draft:
        recipient: any
        subject: any
        body: infer from prompt
    if search_gmail:
        in:inbox
        query: body: any from: any to: any
        """
    response = agent.run(refined_prompt)
    return {"response": response}
