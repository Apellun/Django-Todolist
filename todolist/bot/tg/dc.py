from dataclasses import dataclass
from typing import List
from dataclass_wizard import json_field
from dataclass_wizard import JSONWizard


@dataclass
class Chat(JSONWizard):
    id: int
    first_name: str
    last_name: str
    username: str
    type: str
    
    
@dataclass
class MessageFrom(JSONWizard):
    id: int
    is_bot: bool
    first_name: str
    username: str
    last_name: str = None
    language_code: str = None
    
    
@dataclass
class Message(JSONWizard):
    message_id: int
    from_ : MessageFrom = json_field('from')
    chat: Chat
    date: int
    text: str


@dataclass
class Update(JSONWizard):
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse(JSONWizard):
    ok: bool
    result: List[Update]


@dataclass
class SendMessageResponse(JSONWizard):
    ok: bool
    result: Message