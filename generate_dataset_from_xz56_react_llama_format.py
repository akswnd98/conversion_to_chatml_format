from from_xz56_react_llama_format.converter import Converter as ReactLlamaToChatML
from datasets import load_dataset
import json

if __name__ == '__main__':
  original_dataset = load_dataset('xz56/react-llama')
  converter = ReactLlamaToChatML()

  dataset_json = {
    'train': [{'messages': converter.convert({'question': item['question'], 'trajectory': item['trajectory']})} for item in original_dataset['train']]
  }

  with open('dataset.json', 'w') as f:
    json.dump(dataset_json, f)
