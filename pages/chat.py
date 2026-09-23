
import streamlit as st
from openai import OpenAI

# 페이지 기본 설정 (이 파일만의 설정 — main.py에는 영향 없음)
st.set_page_config(page_title="Ai", page_icon="🤖")
st.title("🤖 AI")

# 비밀 금고(secrets)에서 API 키를 꺼내 접속 준비
client = OpenAI(
    api_key=st.secrets["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# AI의 성격 (화면에는 띄우지 않고 요청에만 함께 보낸다)
SYSTEM_PROMPT = (
    " 다정하고 착한 친구같은 말투 "
    "무조건적인 맞장구나 과장된 칭찬을 사용하지 않고 솔직하게 말해줘. 자연스럽고 편안한 반말로 대화해줘. 유행어나 웃음표현을 추가해줘. 차근차근 설명하고 친절히 말하며 틀린부분은 생각해서 바로잡아. 어떤 이야기를 햐도 함부로 판단하지 마. "
)

# 대화 기록이 없으면 처음 한 번만 만들어 둔다
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 지금까지의 대화를 말풍선으로 다시 그리기 (성격 문장은 숨김)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 채팅 입력창
user_input = st.chat_input("궁금한 것을 물어보세요!")

if user_input:
    # 보낸 말을 기록에 넣고 화면에도 그리기
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 답 받아오기 (실패하면 빨간 오류 화면 대신 안내 문구)
    with st.chat_message("assistant"):
        try:
            stream = client.chat.completions.create(
                model="gemini-3.5-flash-lite",       # 모델 이름은 그대로 유지
                messages=st.session_state.messages,  # 대화 전체를 함께 보내 기억 유지
                stream=True,                         # 글자가 실시간으로 흐르게
            )
            answer = st.write_stream(
                chunk.choices[0].delta.content or ""
                for chunk in stream if chunk.choices
            )
            # AI 답도 기록에 저장 (다음 질문에 이어서 사용)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception:
            st.error("응답을 받지 못했습니다. 잠시 후 다시 보내 주세요.")
          
