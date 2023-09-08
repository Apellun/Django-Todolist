from client import TgClient
import os
from dotenv import load_dotenv

load_dotenv()

cl = TgClient(os.getenv("TELEGRAM_BOT_TOKEN"))
print(cl.get_updates(offset=0, timeout=60))
print(cl.send_message(457035535, "hello"))

