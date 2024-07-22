from tqdm import tqdm
from create_dataset_v2 import clean_text
import pandas as pd

def read_data(path):
    input_file = open(path, 'r', encoding='utf8').read().split('\n')
    return input_file

def process_text(raw_text):
    text = raw_text[14:].strip()
    text = clean_text(text)
    text = f'fill the template: {text}'
    return text.strip()

def main():
    PATH = 'Corpora/en/rephrased_doctext_llama3-instruct_V0.2.txt'
    TRAIN_PATH = 'Corpora/en/train_v3.csv'

    input_file = read_data(PATH)
    processed_texts = []
    for raw_text in input_file:
        processed_texts.append(process_text(raw_text))
    
    df = pd.read_csv(TRAIN_PATH, encoding='utf8')
    inputs = df.input.values.tolist()
    outputs = df.output.values.tolist()

    inputs.extend(processed_texts)
    outputs.extend(outputs)

    augmented_df = pd.DataFrame()
    augmented_df['input'] = inputs
    augmented_df['output'] = outputs

    augmented_df.to_csv('Corpora/en/train_augmented_2_v3.csv', encoding='utf8', index=False)

    
if __name__ == '__main__':
    main()