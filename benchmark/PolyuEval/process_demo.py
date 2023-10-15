# read excel file and save as structured json data
import pandas as pd
import json

# read excel file
df = pd.read_excel('benchmark_demo.xlsx', sheet_name='QA')

def get_ct(category):
    letter = category[0]
    switcher = {
        'A': 'knowledge_memorization',
        'B': 'knowledge_understanding',
        'C': 'knowledge_applying',
        'D': 'knowledge_creating',
    }
    return switcher.get(letter, None)

def get_answer_type(category):
    all_types = ['YesOrNo', 'Sentence', 'List', 'MC']
    switcher = {
        'A-1': 'YesOrNo',
        'A-2': 'List',
        'A-3': 'Sentence',
        'B-1': 'List',
        'B-2': 'MC',
        'C-1': 'List',
        'C-2': 'MC',
        'C-3': 'Sentence',
        'D-1': 'Sentence'
    }
    return switcher.get(category, None)

def get_id(category, index):
    return category.replace('-', '') + '-' + str(index)

def get_matrix_type(category):
    switcher = {
        'YesOrNo': 'F1',
        'Sentence': 'Similarity',
        'List': 'HitRate',
        'MC': 'F1'
    }
    return switcher.get(category, None)

def to_json(df):
    length = len(df)
    result = []

    for i in range(1, length):

        obj = {}
        obj['id'] = get_id(df.loc[i][0], df.loc[i][1])
        obj['cognitive_type'] = get_ct(df.loc[i][0])
        obj['category'] = df.loc[i][0].replace('-', '')
        obj['index'] = str(df.loc[i][1])
        obj['answer_type'] = get_answer_type(df.loc[i][0])
        obj['matrix_type'] = get_matrix_type(obj['answer_type'])
        obj['question'] = df.loc[i][2]

        if obj['answer_type'] != 'Sentence':
            obj['ground_truth'] = str(df.loc[i][3]).split(',')
        else:
            obj['ground_truth'] = df.loc[i][3]

        if obj['answer_type']!='MC' or df.loc[i][4] == 'nan':
            obj['choices'] = []
        else:
            choices = obj['ground_truth']
            obj['choices'] = [
                {"text": df.loc[i][4], "is_correct": True if 'A' in choices else False},
                {"text": df.loc[i][5], "is_correct": True if 'B' in choices else False},
                {"text": df.loc[i][6], "is_correct": True if 'C' in choices else False},
                {"text": df.loc[i][7], "is_correct": True if 'D' in choices else False}
            ]
        result.append(obj)

    return result

result = to_json(df)
with open('benchmark_demo.json', 'w') as f:
    json.dump(result, f, indent=4)