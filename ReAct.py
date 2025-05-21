from dotenv import load_dotenv
from langchain_community.llms import Ollama
import os

load_dotenv('key.env')

#LangChain Hub 가져오기
from langchain import hub

# 환경변수에서 API 키 가져오기
api_key = os.getenv("LangSmith_API_KEY")

#LangChain Hub에서 ReAct의 프롬프트 가져오기
prompt = hub.pull("hwchase17/react", api_key=api_key)

print(prompt)

# #OpenAI 가져오기
# from langchain_openai import OpenAI

# #사용할 LLM 선택
# llm = OpenAI()

# Ollama LLM 객체 생성 (예: llama3 모델)
llm = Ollama(model="llama3")

#SerpAPIWrapper를 통해 도구 모듈 가져오기
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool

#SerpAPIWrapper 인스턴스화
search = SerpAPIWrapper()

#도구 목록 준비
tools = [
    Tool(
        name="Search",
        func=search.run,
        description="LLM이 관련 지식이 없을 때 지식 검색에 사용됩니다."
    ),
]

# craete_react_agent 기능 가져오기
from langchain.agents import create_react_agent

# ReAct 에이전트 생성
agent = create_react_agent(llm, tools, prompt)

# AgentExecutor 가져오기
from langchain.agents import AgentExecutor

# 에이전트와 도구를 전달하여 AgentExecutor 생성
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# # AgentExecutor를 호출하여 입력 데이터 전달
# print("첫 번째 실행 결과:")
# agent_executor.invoke({"input": "보광동의 현재 날씨는 어떤가요?"})

# print("두 번째 실행 결과:")
# agent_executor.invoke({"input": "정수폴리텍의 위치는 어디인가요?"})

from openai import OpenAI

#client 인스턴스 생성하기
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# # chat.completions.create 메서드를 호출하여 응답을 받음
# response = client.chat.completions.create(
#     model="llama3",
#     messages=[
#         {"role": "system", "content": "당신은 사용자가 꽃에 대한 정보를 이해하도록 돕는 지능형 비서이며, JSON 형식의 내용을 출력할 수 있습니다."},
#         {"role": "assistant", "content": "장미꽃은 생일 선물로 인기 있는 선택입니다."},
#         {"role": "user", "content": "인공지능이란 무엇인가요? JSON 형식으로 답변해줘."}
#     ],
#     response_format={"type":"json_object"}
# )

# print(response)
# print(response.choices[0].message.content)

response = client.images.generate(
    model="dall-e-3",
    prompt="A cute baby dog",
    n=1,
    size="512x512",
    quality="standard"
)

image_url = response.data[0].url

import requests

image = requests.get(image_url).content

from IPython.display import Image

Image(image)

