from utils.read_jsonl import get_jsonl
from scipy import stats
from operator import countOf

def get_dataset_statistics(path):
    # read data
    jsonl = get_jsonl(path)
    
    # number of instances
    instances = len(jsonl)
    
    # Templates mean
    templates_per_instance = [len(obj['templates']) for obj in jsonl]
    templates_mean = sum(templates_per_instance) / instances

    # Templates mode
    templates_mode = stats.mode(templates_per_instance)

    # Max number of templates
    template_max = max(templates_per_instance)

    print(f'\tInstances: {instances}\n\tMean: {templates_mean}\n\tMode: {templates_mode}\n\tMax: {template_max}\n\tTemplates: {sum(templates_per_instance)}\n')

    get_templates_statistics(jsonl)

    get_char_count(jsonl)

    get_word_count(jsonl)

def get_templates_statistics(jsonl):
    full_classes = []
    for obj in jsonl:
        templates = obj['templates']
        if len(templates) > 0:
            for template in templates:
                temp_type = template['incident_type']
                full_classes.append(temp_type)
    
    classes = sorted(set(full_classes))
    for class_ in classes:
        print(f'\t{class_}: {countOf(full_classes,class_)}')

def get_char_count(jsonl):
    char_len_per_instance = [len(obj['doctext']) for obj in jsonl]
    mean_char_len = sum(char_len_per_instance) / len(jsonl)
    print(f'\n\tMean char len: {mean_char_len}')
    print(f'\tMax char len: {max(char_len_per_instance)}')

def get_word_count(jsonl):
    word_len_per_instance = [len(obj['doctext'].split(' ')) for obj in jsonl]
    mean_word_len = sum(word_len_per_instance) / len(jsonl)
    print(f'\n\tMean word len: {mean_word_len}')
    print(f'\tMax word len: {max(word_len_per_instance)}')


def main():
    BASE_PATH = 'data/multimuc_v1.0/en'
    partitions = ['train', 'dev', 'test']

    for partition in partitions:
        path = f'{BASE_PATH}/{partition}.jsonl'
        print(f'Partition: {partition}')
        get_dataset_statistics(path)

if __name__ == '__main__':
    main() 
