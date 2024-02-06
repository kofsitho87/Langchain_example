import streamlit as st
import tiktoken
from loguru import logger

from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import UnstructuredPowerPointLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS

# from streamlit_chat import message
from langchain.callbacks import get_openai_callback
from langchain.memory import StreamlitChatMessageHistory


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def main():
    st.set_page_config(
    page_title="DirChat",
    page_icon=":books:")

    st.title("이미지를 통해 보는 역사박물관 :red[Museum of History] :books:")

    st.session_state.conversation = get_conversation_chain()

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    if 'messages' not in st.session_state:
        st.session_state['messages'] = [{"role": "assistant", 
                                        "content": "안녕하세요!이미지 주소를 입력주세요."}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    history = StreamlitChatMessageHistory(key="chat_messages")


    # Chat logic
    if query := st.chat_input("이미지 URL"):
        st.session_state.messages.append({"role": "user", "content": query})

        with st.chat_message("user"):
            st.markdown(query)
            # 이미지 URL을 표시
            st.image(query, caption="입력한 이미지")

        with st.chat_message("assistant"):
            llm = st.session_state.conversation

            with st.spinner("Thinking..."):
                result = get_chat_result(llm, query)
                # result = llm.invoke(query)

                with get_openai_callback() as cb:
                    st.session_state.chat_history = result.content
                response = result.content

                st.markdown(response)
                    


# Add assistant message to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def get_conversation_chain():
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro-vision", 
        google_api_key="AIzaSyD-54IdImuIDLbNrCQ970l_MkDPOd0-Nns",
        temperature=0
    )
    return llm

def get_chat_result(llm, image_url):
    message = HumanMessage(
        content=[
            {
                "type": "text",
                "text": """
                1. 이미지가 어떤 역사적인 유물인지 명칭을 정확히 알려주고
                2. 이미지가 역사적인 유물이나 장소라면 해당 이미지에 대한 역사적인 설명을 초등학생이 알아듣기 쉽게 선생님의 역할로써 학생에게 설명해줘, 내용은 500자내외로 해줘, 참고할만한 링크가 있으면 링크주소도 첨부해줘
                """,
            },
            {"type": "image_url", "image_url": image_url},
        ]
    )
    return llm.invoke([message])

if __name__ == '__main__':
    main()