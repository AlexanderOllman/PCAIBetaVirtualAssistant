from langchain.schema import AIMessage, HumanMessage
from langchain_nvidia_ai_endpoints import ChatNVIDIA
import gradio as gr
import os

url = "https://llama3-8b-instruct-1xgpu-predictor-admin-835cc1e3.prod.discover.hpepcai.com/v1"
model = "meta/llama3-8b-instruct"
nvidia_api_key = os.getenv("AUTH_TOKEN")
llm = ChatNVIDIA(base_url=url, model=model, api_key=nvidia_api_key)

def predict(message, history):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))
    gpt_response = llm.invoke(history_langchain_format)
    return gpt_response.content

gr.ChatInterface(predict).launch(server_name="0.0.0.0", server_port=8080)