from datetime import datetime

from revChatGPT.revChatGPT import Chatbot

#
# from src.main import CONFIG
#
# # TODO: Change way to get session token.
# # login account and wait response from Open AI
# # /api/auth/session
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/108.0.0.0 Edg/108.0.1462.46"
# }
# resp = requests.get("{}/api/auth/session".format(CONFIG["openai"]["base_url"]), headers=headers)

config = {
    "session_token": ""
}

chatbot = Chatbot(config, conversation_id=None)


def chat(msg):
    print("正在开始计算问题回答所需时间")
    start = datetime.timestamp(datetime.now())
    message = chatbot.get_chat_response(msg)['message']
    end = datetime.timestamp(datetime.now())

    return int(end - start), message


if __name__ == '__main__':
    print(chatbot.get_chat_response("hello")["message"])
