from langchain.schema import AIMessage, HumanMessage
# from langchain_nvidia_ai_endpoints import ChatNVIDIA
import gradio as gr
import os
import json
import aiohttp
import logging
import requests

def predict(message, history, request: gr.Request):
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))
    history_langchain_format.append(HumanMessage(content=message))

    url = "https://llama3-8b-instruct-1xgpu-predictor-admin-835cc1e3.prod.discover.hpepcai.com/v1"
    model = "meta/llama3-8b-instruct"

    data = {
    "model": model,
    "messages": history_langchain_format,
    "max_tokens": 100,
    "temperature": 1
    }

    headers = {"Authorization": "Bearer " + request.headers["authorization"]}
    response = requests.post(url, json=data, headers=headers, verify=False)
    result = json.loads(response.text)

    # print(result["choices"][0]["message"]["content"].strip())
    # nvidia_api_key = request.headers.get("authorization")
    # llm = ChatNVIDIA(base_url=url, model=model, api_key=nvidia_api_key)
    # gpt_response = llm.invoke(history_langchain_format).content
    gpt_response = result["choices"][0]["message"]["content"].strip()
    return gpt_response
gr.ChatInterface(predict).launch(server_name="0.0.0.0", server_port=8080)