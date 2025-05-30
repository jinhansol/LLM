# 환경 변수 적재하기
from dotenv import load_dotenv

load_dotenv("key.env")

# OpenAI 인스턴스 생성
from openai import OpenAI

client = OpenAI()

# #도우미 생성
# assistant = client.beta.assistants.create(
#     name="꽃 가격 계산기",
#     instructions="당신은 저에게 꽃의 가격을 계산해줄 수 있습니다.",
#     tools=[{"type": "code_interpreter"}],
#     model="gpt-4o-mini"
# )

# # 생성한 도우미 목록 얻기
# assistants = client.beta.assistants.list()

# # 도우미 출력
# print(assistants)

# 대화 흐름 생성
thread = client.beta.threads.create()

# # 대화 흐름에 메시지 추가
# message = client.beta.threads.messages.create(
#     thread_id=thread.id,
#     role="user",
#     content="각 꽃다발의 가격을 원가에 20%를 더한 가격으로 책정합니다. 원가가 1600원일 때, 제 판매 가격은 얼마인가요?"
# )

# #메시지 목록 가져오기
# messages = client.beta.threads.messages.list(
#     thread_id='thread_9Hto68hM5lmqOqB8vXLTZDqU'
# )

# #대화 흐름 출력
# print(messages)

# # 실행 세션 생성
# run = client.beta.threads.runs.create(
#     thread_id=thread.id,
#     assistant_id=assistant.id,
#     instructions="질문에 답변해주세요."
# )

# # 실행 세션 상태 다시 가져오기
# run = client.beta.threads.runs.retrieve(
#     thread_id=thread.id,
#     run_id=run.id
# )

# # 실행 세션 출력
# print(run)

# 대화 흐름과 도우미 ID 지정
thread_id = 'thread_9Hto68hM5lmqOqB8vXLTZDqU'
assistant_id = 'asst_2gzQ5w8vP2QaS2TMnvgD7ws2'

# 실행 세션 생성
run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    instructions="질문에 답변해주세요."
)

# 확인 간격 시간 설정(5초)
polling_interval = 5

# # 실행 세션 상태 확인 시작
# import time
# while True:
#     run = client.beta.threads.runs.retrieve(
#         thread_id=thread_id,
#         run_id=run.id
#     )

#     # 실행 세션 객체의 속성에 직접 접근
#     status = run.status

#     # print(F"Run Status: {status}")

#     # 실행 세션의 상태가 'completed', 'failed', 'expired'일 경우 순환 종료
#     if status in ['completed', 'failed', 'expried']:
#         break

#     # 확인 간격 시간 대기 후 반복
#     time.sleep(polling_interval)

# # 실행 세션 결과 처리
# if status == 'completed':
#     print("Run completed successfully.")
# elif status in ['failed', 'expired']:
#     print("Run failed or expired.")

# 대화 흐름 ID 설정
thread_id = 'thread_9Hto68hM5lmqOqB8vXLTZDqU'

# 대화 흐름에서 메시지 읽기
messages = client.beta.threads.messages.list(
    thread_id=thread_id
)

# # 메시지 출력
# print(messages)

#데이터 파일 적재 및 내용 표시
import pandas as pd

file_path = 'sales_data.csv'
sales_data = pd.read_csv(file_path)

# 파일 생성
file = client.files.create(
    file=open(file_path, 'rb'),
    purpose='assistants',
)

# 파일을 포함한 도우미 생성
assistant = client.beta.assistants.create(
    instructions='데이터 과학 도우미로서, 주어진 데이터와 요청에 따라 적절한 코드를 작성하고 적절한 시각화를 생성할 수 있습니다.',
    model="gpt-4o-mini",
    tools=[{'type': 'code_interpreter'}],
    tool_resources={
        'code_interpreter': {
            'file_ids': [file.id]
        }
    }
)

# print(assistant)

# 대화 흐름 생성
thread = client.beta.threads.create(
    messages=[{
        "role": "user",
        "content": "2022년부터 2025년까지 각 분기의 총 판매액을 계산하고, 이를 다른 제품으로 시각화하여 선 그래프로 표시하세요. 제품의 선 색상은 각각 빨강, 파랑, 녹색으로 설정하세요.",
        "attachments": [
            {
                "file_id": file.id,
                "tools": [
                    {"type": "code_interpreter"}
                ]
            }
        ]
    }]
)

# print(thread)

# 실행 세션 생성
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id,
)

# # 실행 세션 출력
# print(run)

import time

while True:
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    try:
        #이미지 파일 생성 확인
        if messages.data[0].content[0].image_file:
            print('차트가 생성되었습니다!')

            if messages.data and messages.data[0].content:
                print('현재 메시지:', messages.data[0].content[0])
            break
    except:
        time.sleep(10)

        print('도우미가 차트를 열심히 작성하고 있습니다...')

        if messages.data and messages.data[0].content:
            print('현재 메시지:', messages.data[0].content[0])

    # 순환 전 잠시 대기
    time.sleep(5)

# 파일을 PNG 형식으로 변환하는 함수
def convert_file_to_png(file_id, write_path):
    data = client.files.content(file_id)
    data_bytes = data.read()

    with open(write_path, 'wb') as file:
        file.write(data_bytes)

# 첫 번째 메시지에서 이미지 파일 UD 가져오기
plot_file_id = messages.data[0].content[0].image_file.file_id
image_path = '태진_도서_판매.png'

# 파일을 PNG로 변환
convert_file_to_png(plot_file_id, image_path)

# 차트 업로드
plot_file = client.files.create(
    file=open(image_path, 'rb'),
    purpose='assistants'
)