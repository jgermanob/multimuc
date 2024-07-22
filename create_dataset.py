import pandas as pd
from utils.read_jsonl import get_jsonl
import re

def clean_text(raw_text):
    text = re.sub(r'[^\w\s]', '', raw_text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()



def get_templates(json_object):
    templates = json_object['templates']
    if len(templates) < 1:
        return '<extra_id_0> None <extra_id_1>'
    output_text = '<extra_id_0> '
    index = 1
    for template in templates:
        template_type = template['incident_type']
        output_text += f'{template_type} <extra_id_{index}> '
        index += 1
        print(f'Template type: {template_type}')
        
        # PerpInd
        print(f'PerpInd:')
        slots = template['PerpInd']
        if len(slots) > 0:
            slot_list = []
            for s in slots:
                print(f'\t{s}')
                #output_text+= f'{pi[0][0]} <extra_id_{index}> '
                slot_list.append(s[0][0])
                #index += 1
            if len(slot_list) > 1:
                tem_output_text = ', '.join(slot_list).strip()
                output_text += f'{tem_output_text} <extra_id_{index}> '
                index += 1
            else:
                output_text+= f'{slot_list[0]} <extra_id_{index}> '
                index += 1
        else:
            output_text += f'None <extra_id_{index}> '
            index += 1
        
        #PerpOrg
        print(f'PerpOrg')
        slots = template['PerpOrg']
        if len(slots) > 0:
            slot_list = []
            for s in slots:
                print(f'\t{s}')
                #output_text+= f'{pi[0][0]} <extra_id_{index}> '
                slot_list.append(s[0][0])
                #index += 1
            if len(slot_list) > 1:
                temp_output_text = ', '.join(slot_list).strip()
                output_text += f'{temp_output_text} <extra_id_{index}> '
                index += 1
            else:
                output_text+= f'{slot_list[0]} <extra_id_{index}> '
                index += 1
        else:
            output_text += f'None <extra_id_{index}> '
            index += 1
        
        #Target
        print(f'Target')
        slots = template['Target']
        if len(slots) > 0:
            slot_list = []
            for s in slots:
                print(f'\t{s}')
                #output_text+= f'{pi[0][0]} <extra_id_{index}> '
                slot_list.append(s[0][0])
                #index += 1
            if len(slot_list) > 1:
                temp_output_text = ','.join(slot_list).strip()
                output_text += f'{temp_output_text} <extra_id_{index}> '
                index += 1
            else:
                output_text+= f'{slot_list[0]} <extra_id_{index}> '
                index += 1
        else:
            output_text += f'None <extra_id_{index}> '
            index += 1

        # Victim
        print(f'Victim')
        slots = template['Victim']
        if len(slots) > 0:
            slot_list = []
            for s in slots:
                print(f'\t{s}')
                #output_text+= f'{pi[0][0]} <extra_id_{index}> '
                slot_list.append(s[0][0])
                #index += 1
            if len(slot_list) > 1:
                temp_output_text = ', '.join(slot_list).strip()
                output_text += f'{temp_output_text} <extra_id_{index}> '
                index += 1
            else:
                output_text+= f'{slot_list[0]} <extra_id_{index}> '
                index += 1
        else:
            output_text += f'None <extra_id_{index}> '
            index += 1

        # Weapon
        print(f'Weapon')
        slots = template['Weapon']
        if len(slots) > 0:
            slot_list = []
            for s in slots:
                print(f'\t{s}')
                #output_text+= f'{pi[0][0]} <extra_id_{index}> '
                slot_list.append(s[0][0])
                #index += 1
            if len(slot_list) > 1:
                temp_output_text = ', '.join(slot_list).strip()
                output_text += f'{temp_output_text} <extra_id_{index}> '
                index += 1
            else:
                output_text+= f'{slot_list[0]} <extra_id_{index}> '
                index += 1
        else:
            output_text += f'None <extra_id_{index}> '
            index += 1
    
    return output_text.strip()

def get_processed_instance(json_object):
    template_types = ['arson', 'attack', 'bombing', 'forced work stoppage', 'kidnapping', 'robbery', 'attack/bombing', 'bombing/attack']
    text = json_object['doctext']
    text = clean_text(text)
    print(text)

    # Input
    template_string = ', '.join(template_types).strip()
    input_string = f'<extra_id_0> {template_string} <extra_id_1> {text} <extra_id_2>'

    # Output
    output_string = get_templates(json_object)

    return input_string, output_string

def main():
    LANG = 'en'
    BASE_PATH = f'data/multimuc_v1.0/{LANG}'

    partitions = ['train', 'dev', 'test']

    full_inputs = []
    full_outputs = []

    for partition in partitions:
        path = f'{BASE_PATH}/{partition}.jsonl'
        print(f'Partition: {partition}')
        full_inputs = []
        full_outputs = []

        jsonl = get_jsonl(path)
        for line in jsonl:
            input_string, output_string = get_processed_instance(line)
            full_inputs.append(input_string)
            full_outputs.append(output_string)
            #break
        #break
        
        df = pd.DataFrame()
        df['input'] = full_inputs
        df['output'] = full_outputs

        NEW_PATH = f'Corpora/{LANG}'
        csv_path = f'{NEW_PATH}/{partition}.csv'
        df.to_csv(csv_path, encoding='utf8', index=False)
    

if __name__ == '__main__':
    main() 



