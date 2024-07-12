from converter import Converter as ProtoConverter
from typing import TypedDict, Literal
from from_xz56_react_llama_format.converter.trajectory_converter import NumberingRemover, FinishConverter, ActionConverter, ChatMLGeneratorFromTrajectory
from chatml import ChatMLItem

class Input (TypedDict):
  question: str
  trajectory: str

class Converter (ProtoConverter[Input, list[ChatMLItem]]):
  def __init__ (self):
    self.trajectory_converter = NumberingRemover() | FinishConverter() | ActionConverter() | ChatMLGeneratorFromTrajectory()

  def convert (self, input: Input) -> list[ChatMLItem]:
    return [{'role': 'user', 'content': f'Question:{input['question']}'}] + self.trajectory_converter.convert(input['trajectory'])
