from transformers import T5ForConditionalGeneration
from transformers import T5Tokenizer
from dataset.t5_dataset import T5_templateFilling_dataset
from torch.utils.data import DataLoader
import pandas as pd
import torch
from tqdm import tqdm
from torch import cuda
import re
from transformers import GenerationConfig

import transformers
import json 

transformers.logging.set_verbosity_error()

TEST_DATA_PATH = 'Corpora/en/test_v2.csv'
device = 'cuda' if cuda.is_available() else 'cpu'


def generate_row_template(dataloader: DataLoader, model: T5ForConditionalGeneration, tokenizer:T5Tokenizer):
    model.eval()
    decoded_outputs = []
    config = GenerationConfig(max_new_tokens=512,
                              num_beams=1)
    with torch.no_grad():
        for batch in tqdm(dataloader):
            ids = batch['input_ids'].to(device, dtype=torch.long)
            mask = batch['attention_mask'].to(device, dtype=torch.long)
            batch_outputs = model.generate(input_ids = ids, attention_mask=mask, generation_config=config)
            batch_decoded_outputs = tokenizer.batch_decode(batch_outputs, skip_special_tokens=True)
            decoded_outputs.extend(batch_decoded_outputs)
    
    #print(f'Decoded outputs: {len(decoded_outputs)}')
    return decoded_outputs

def process_slot(slot):
    slot = slot.split(':')[1].strip()
    if slot == 'None':
        return []
    else:
        if len(slot.split(',')) > 1:
            slot = [[s] for s in slot.split(',')]
        else:
            slot = [[slot]]
    return slot


def get_template_info(raw_template):
    raw_template = raw_template.strip()
    slots = raw_template.split('|')
    if len(slots) == 6:
        incident_type, perpInd, perpOrg, target, victim, weapon = slots
        
        incident_type = incident_type.split(':')[1].strip()
        
        perpInd = process_slot(perpInd)
        perpOrg = process_slot(perpOrg)
        target = process_slot(target)
        victim = process_slot(victim)
        weapon = process_slot(weapon)

        #print(f'\tinicident_type: {incident_type}\n\tPerpInd: {perpInd}\n\tPerpOrg: {perpOrg}\n\tTarget: {target}\n\tVictim: {victim}\n\tWeapon: {weapon}\n')
        return {'incident_type': incident_type,
                'PerpInd': perpInd,
                'PerpOrg': perpOrg,
                'Target': target,
                'Victim': victim,
                'Weapon': weapon}

    else:
        return None


def create_jsonl(raw_output):
    if isinstance(raw_output, float):
        return []
    templates = raw_output.split('  ')
    pred_templates = []
    for index, template in enumerate(templates):
        #print(f'Template {index+1}:')
        template = get_template_info(template)
        if template:
            pred_templates.append(template)

    return pred_templates

def main():
    """
    model_checkpoint = 'google-t5/t5-base'
    tokenizer = T5Tokenizer.from_pretrained(model_checkpoint)
    test_df = pd.read_csv(TEST_DATA_PATH, encoding='utf8')
    test_dataset = T5_templateFilling_dataset(test_df, tokenizer)
    test_dataloader = DataLoader(test_dataset, batch_size=4)
    model = T5ForConditionalGeneration.from_pretrained('models/T5/Flan_T5_muc4_en_v3')

    decoded_outputs = generate_row_template(test_dataloader, model, tokenizer)
    test_df['decoded_outputs'] = decoded_outputs
    test_df.to_csv('Corpora/en/generation/flan_t5_test_greedy_v3.csv', encoding='utf8', index=False)

    """
    temp_path = 'Corpora/en/generation/flan_t5_test_greedy_v3.csv'
    test_df = pd.read_csv(temp_path, encoding='utf8')
    raw_outputs = test_df.decoded_outputs.values.tolist()

    doc_id = 30001
    output = {}
    for raw_output in raw_outputs:
        #print(f'\n{raw_output}')
        generated_templates = create_jsonl(raw_output)
        output[f"{str(doc_id)}"] = {'pred_templates': generated_templates}
        doc_id += 1
        if doc_id == 30101:
            doc_id = 40001
    
    with open('Corpora/en/test_preds.json', 'w') as outfile:
        json.dump(output, outfile)
        
        
    
    

if __name__ == '__main__':
    main()
