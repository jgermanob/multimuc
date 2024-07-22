import jsonlines

def get_jsonl(path):
    json_list = []
    with jsonlines.open(path) as reader:
        for object in reader:
            json_list.append(object)
    return json_list


