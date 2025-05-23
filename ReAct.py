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

# from ollama import generate
# from IPython.display import Image, display

# image = generate(
#     model='llava:13b',
#     prompt = 'A cute baby dog',
#     max_tokens=1024
# )

# with open('output.png', 'wb') as f:
#     f.write(image)

# display(Image(filename='output.png'))

# #출력을 문자열로 변환하기 위한 출력 분석기
# from langchain_core.output_parsers import StrOutputParser
# #대화 프롬프트 템플릿을 생성하기 위한 모듈
# from langchain_core.prompts import ChatPromptTemplate

# #프롬프트 템플릿 생성
# prompt = ChatPromptTemplate.from_template( "{topic}에 대한 이야기를 들려주세요.")

#Ollama Llma 3모델 객체 생성
model = Ollama(model="llama3", temperature=0.1)

# #출력 파서 초기화
# output_parser = StrOutputParser()

# #체인 연결
# chain = prompt | model | output_parser

# #실행
# message = chain.invoke({"topic": "수선화"})
# print(message)

# #프롬프트 템플릿 설정
# from langchain.prompts import PromptTemplate

# prompt = PromptTemplate.from_template("{flower}의 꽃말은?")

# #출력 분석기 설정
# from langchain.schema.output_parser import StrOutputParser

# output_parser = StrOutputParser()

# #연쇄 구성
# chain = prompt | model | output_parser

# #연쇄를 실행하고 결과를 출력력
# result = chain.invoke({"flower": "라일락"})

# print(result)

# #'꽃말의 비밀 정원 이야기' 문서 적재
# from llama_index.core import SimpleDirectoryReader

# documents = SimpleDirectoryReader("./data").load_data()

# #Ollama LLM 및 임베딩 모델 지정
# from llama_index.embeddings.ollama import OllamaEmbedding
# embed_model = OllamaEmbedding(model_name="llama3")

# # #문서의 색인 생성
# # from llama_index.core import VectorStoreIndex
# # index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

# #요청 엔진 생성
# agent = index.as_query_engine(llm=llm)

# # #요청 예제
# # response = agent.query("꽃말의 비밀 정원의 직원에게는 몇 가지 역할이 있나요?")
# # print("꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요?", response)
# # response = agent.query("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?")
# # print("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?", response)

# #색인을 로컬에 저장
# index.storage_context.persist()

import ollama

# #시스템 프롬프트(역할 지시시)
# system_prompt = "당신은 저에게 꽃의 가격을 계산해줄 수 있습니다. 필요한 경우 코드를 작성해 설명해 주세요."

# #사용자 질문
# user_message = "장미 10송이의 가격을 계산해줘."

# #Ollama3 모델로 대화 요청
# response = ollama.chat(
#     model="llama3",
#     messages=[
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": user_message},
#     ],
# )

# print(response["message"]["content"])

#설치된 모델 목록 가져오기
models = ollama.list()
print(models)

# #모델에 프롬프트 보내기 예시
# response = ollama.chat(
#     model="llama3",
#     messages=[
#         {"role": "user", "content": "Hello, what can you do?"}
#     ]
# )
# print(response["message"]["content"])

messages = [
    {"role": "user", "content": "안녕!"},
]
response = ollama.chat(model="llama3", messages=messages)
print(response["message"]["content"])

# 답변을 messages에 추가
messages.append({"role": "assistant", "content": response["message"]["content"]})

#다음 질문 추가
messages.append({"role": "user", "content": "오늘 날씨 어때?"})
response = ollama.chat(model="llama3", messages=messages)
print(response["message"]["content"])