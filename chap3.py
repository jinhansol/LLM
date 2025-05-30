from dotenv import load_dotenv
load_dotenv("key.env")

# OpenAI 가져오기
from openai import OpenAI

# client 인스턴스 생성하기
client = OpenAI()

# # chat.completions.create 메서드를 호출하여 응답을 받음
# response = client.chat.completions.create(
#     model="gpt-4o-mini",
#     response_format={
#         "type": "json_object"
#     },
#     messages=[
#         {"role": "system", "content": "당신은 사용자가 꽃에 대한 정보를 이해하도록 돕는 지능형 비서이며, JSON 형식의 내용을 출력할 수 있습니다."},
#         {"role": "user", "content": "생일 선물로 어떤 꽃이 가장 좋을까요?"},
#         {"role": "assistant", "content": "장미꽃은 생일 선물로 인기 있는 선택입니다."},
#         {"role": "user", "content": "배송세는 얼마나 걸리나요?"}
#     ]
# )
# print(response)
# print(response.choices[0].message.content)

# # DALL`E 3에 이미지 생성 요청
# response = client.images.generate(
#     model="dall-e-3",
#     prompt="'꽃말의 비밀 정원' 전자상거래 앱의 새해 장미꽃 홍보 포스터, 문구도 포함해서",
#     size="1024x1024",
#     quality="standard",
#     n=1
# )

# # 이미지 URL 가져오기
# image_url = response.data[0].url

# # 이미지 읽어오기
# import requests

# image = requests.get(image_url).content

# # Jupyter Notebook에서 이미지 표시
# from IPython.display import Image

# Image(image)

# # 출력을 문자열로 변환하기 위한 출력 분석기
# from langchain_core.output_parsers import StrOutputParser

# # 대화 프롬프트 템플릿을 생성하기 위한 모듈
# from langchain_core.prompts import ChatPromptTemplate

# # OpenAI GPT모델을 호출하기 위한 모듈
# from langchain_openai import ChatOpenAI

# # {topic}은 나중에 특정 주제가 삽입될 위치표시자
# # 주제에 관한 이야기를 요청하는 대화 프롬프트 템플릿 생성
# prompt = ChatPromptTemplate.from_template("{topic}에 대한 이야기를 들려주세요.")

# # OpenAI GPT-4 모델을 사용하여 ChatOpenAI 객체 초기화
# model = ChatOpenAI(model = "gpt-4")

# # 모델의 출력을 문자열을 변환하기 위한 출력 파서 초기화
# output_parser = StrOutputParser()

# '''
# 파이프라인 연산자(|)를 사용하여 각 처리 단계를 연결해 하나의 처리 구조로 연동
# prompt는 구체적인 프롬프트 텍스트를 생성하고,
# model은 그 텍스트에 대한 응답을 생성하며,
# output_parser는 그 응답을 처리하여 문자열로 변환
# '''
# chain = prompt | model | output_parser

# # 연쇄를 호출하고, 주제 "수선화"를 입력하여 이야기 생성 작업 실행
# message = chain.invoke({"topic": "수선화"})

# # 결과 출력
# print(message)

# # 프롬프트 템플릿 설정
# from langchain.prompts import PromptTemplate

# prompt = PromptTemplate.from_template("{flower}의 꽃말은?")

# # LLM 설정
# from langchain_openai import OpenAI

# model = OpenAI()

# # 출력 분석기 설정
# from langchain.schema.output_parser import StrOutputParser

# output_parser = StrOutputParser()

# # 연쇄 구성
# chain = prompt | model | output_parser

# # 연쇄를 실행하고 결과를 출력
# result = chain.invoke({"flower": "라일락"})

# print(result)

# '꽃말의 비밀 정원 이야기' 문서 적재
from llama_index.core import SimpleDirectoryReader

documents = SimpleDirectoryReader("data").load_data()

# 문서의 색인 생성
from llama_index.core import VectorStoreIndex
index = VectorStoreIndex.from_documents(documents)

# 요청 엔진 생성
agent = index.as_query_engine()

# 요청 예제
response = agent.query("꽃말의 비밀 정원의 직원에게는 몇 가지 역할이 있나요?")
print("꽃말의 비밀 정원의 직원들에게는 몇 가지 역할이 있나요?", response)
response = agent.query("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?")
print("꽃말의 비밀 정원의 에이전트 이름은 무엇인가요?", response)