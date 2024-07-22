import pandas as pd
from utils.read_jsonl import get_jsonl
import re
import orjsonl

def clean_text(raw_text):
    text = re.sub(r'[^\w\s]', '', raw_text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_templates(json_object):
    templates = json_object['templates']
    if len(templates) < 1:
        return []
    template_types = []
    for template in templates:
        template_type = template['incident_type']
        template_types.append(template_type)

    return template_types

def get_processed_instance(json_object):
    template_types = ['arson', 'attack', 'bombing', 'forced work stoppage', 'kidnapping', 'robbery', 'attack/bombing', 'bombing/attack']
    text = json_object['doctext']
    text = clean_text(text)
    #print(text)

    # Input
    input_string = f'{text}'

    # Output
    output_string = get_templates(json_object)

    return input_string, output_string

def get_labels(example):
    arson = False
    attack = False
    attack_bombing = False
    bombing = False
    bombing_attack = False
    forced_work = False
    kidnapping = False
    robbery = False
    for element in example:
        if element == 'arson':
            arson = True
        elif element == 'attack':
            attack = True
        elif element == 'attack/bombing':
            attack_bombing = True
        elif element == 'bombing':
            bombing = True
        elif element == 'bombing/attack':
            bombing_attack = True
        elif element == 'forced work stoppage':
            forced_work = True
        elif element == 'kidnapping':
            kidnapping = True
        elif element == 'robbery':
            robbery = True
                                                               
    return arson, attack, attack_bombing, bombing, bombing_attack, forced_work, kidnapping, robbery


def main():
    LANG = 'en'
    BASE_PATH = f'data/multimuc_v1.0/{LANG}'

    partitions = ['train', 'dev', 'test']

    full_inputs = []
    full_outputs = []
    
    template_types = ['arson', 'attack', 'bombing', 'forced work stoppage', 
                      'kidnapping', 'robbery', 'attack/bombing', 'bombing/attack']
    
    template_types = sorted(template_types)
    
    for partition in partitions:
        path = f'{BASE_PATH}/{partition}.jsonl'
        print(f'Partition: {partition}')
        full_inputs = []
        full_outputs = []

        jsonl = get_jsonl(path)
        processed_jsonl = []
        for line in jsonl:
            input_string, output_string = get_processed_instance(line)
            docid = line['docid']
            arson, attack, attack_bombing, bombing, bombing_attack, forced_work, kidnapping, robbery = get_labels(output_string)
            jsonl_line = {'docid': docid,
                          'doctext': input_string,
                          'arson': arson,
                          'attack': attack,
                          'attack/bombing': attack_bombing,
                          'bombing': bombing,
                          'bombing/attack': bombing_attack,
                          'forced work stoppage': forced_work,
                          'kidnapping': kidnapping,
                          'robbery': robbery
                          }
            processed_jsonl.append(jsonl_line)
            print(jsonl_line)
        
        NEW_PATH = f'Corpora/{LANG}'
        jsonl_path = f'{NEW_PATH}/{partition}.jsonl'
        orjsonl.save(jsonl_path, processed_jsonl)
        
if __name__ == '__main__':
    main() 

