from converter import Converter
from chatml import ChatMLItem
import re

class NumberingRemover (Converter[str, str]):
  def convert (self, input: str) -> str:
    ret = input
    ret = re.sub('Thought [0-9]+:', 'Thought:', ret)
    ret = re.sub('Action [0-9]+:', 'Action:', ret)
    ret = re.sub('Observation [0-9]+:', 'Observation:', ret)
    return ret

class FinishConverter (Converter[str, str]):
  def convert (self, input: str) -> str:
    return re.sub('Action: Finish\[(.+)\]', lambda str_match: f'Final Answer: {str_match.groups()[0]}', input)

class ActionConverter (Converter):
  def convert (self, input: str) -> str:
    return re.sub('Action: (.+)\[(.+)\]', lambda str_match: f'Action: {str_match.groups()[0]}\nAction Input: {str_match.groups()[1]}', input)

class ChatMLGeneratorFromTrajectory (Converter[str, list[ChatMLItem]]):
  def convert (self, input: str) -> list[dict[str, str]]:
    thought_indices = self.get_pattern_indices(input, 'Thought:')
    observation_indices = self.get_pattern_indices(input, 'Observation:')
    final_answer_str = input[thought_indices[-1]: ]
    assistant_strs = [input[thought_index: observation_index - 1] for thought_index, observation_index in zip(thought_indices[: -1], observation_indices)]
    user_strs = [input[observation_index: thought_index - 1] for observation_index, thought_index in zip(observation_indices, thought_indices[1: ])]
    ret = []
    for assistant_str, user_str in zip(assistant_strs, user_strs):
      ret.append({'role': 'assistant', 'content': assistant_str})
      ret.append({'role': 'user', 'content': user_str})
    ret.append({'role': 'assistant', 'content': final_answer_str})
    return ret

  def get_pattern_indices (self, input: str, pattern: str):
    match_iter = re.finditer(pattern, input)
    match_objs = [match_obj for match_obj in match_iter]
    spans = [match_obj.span() for match_obj in match_objs]
    return [span[0] for span in spans]
