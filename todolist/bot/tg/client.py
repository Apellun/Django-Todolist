from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
import requests


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url_base = self.get_url("getUpdates")
        url = f"{url_base}?timeout={timeout}&offset={offset}"
        response = requests.get(url).json()
        update = GetUpdatesResponse.from_dict(response)
        return update
            
    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url_base = self.get_url("sendMessage")
        url = f"{url_base}?chat_id={chat_id}&text={text}"
        response = requests.get(url).json()
        result = SendMessageResponse.from_dict(response)
        return result
        