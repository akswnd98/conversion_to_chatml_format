from typing import TypedDict, Literal

class ChatMLItem (TypedDict):
  role: Literal['user'] | Literal['assistant']
  content: str
