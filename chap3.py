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

# DALL`E 3에 이미지 생성 요청
response = client.images.generate(
    model="dall-e-3",
    prompt="'꽃말의 비밀 정원' 전자상거래 앱의 새해 장미꽃 홍보 포스터, 문구도 포함해서",
    size="1024x1024",
    quality="standard",
    n=1
)

# 이미지 URL 가져오기
image_url = response.data[0].url

# 이미지 읽어오기
import requests

image = requests.get(image_url).content

# Jupyter Notebook에서 이미지 표시
from IPython.display import Image

Image(image)