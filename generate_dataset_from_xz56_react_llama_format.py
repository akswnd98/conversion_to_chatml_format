from from_xz56_react_llama_format.converter import Converter as ReactLlamaToChatML
from datasets import load_dataset
import json

if __name__ == '__main__':
  original_dataset = load_dataset('xz56/react-llama')

  excluded_indices = [651]
  selected_indices = [i for i in range(len(original_dataset['train']))]
  for excluded_index in excluded_indices:
    selected_indices.remove(excluded_index)
  selected_dataset = original_dataset['train'].select(selected_indices)

  converter = ReactLlamaToChatML()

  dataset_json = {
    'train': [{'messages': converter.convert({'question': item['question'], 'trajectory': item['trajectory']})} for item in selected_dataset]
  }

  with open('dataset.json', 'w') as f:
    json.dump(dataset_json, f)
