import json

def read_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()

def save_json(obj,path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(obj,f)

def read_wn_data_words(path):
    lines = read_lines(path)
    data = []
    for line in lines[29:]:
        data.append(line.split(' ')[4].replace('_','-'))
    return data

def read_wn_exc(path):
    lines = read_lines(path)
    exc = {}
    for line in lines:
        v_v = line.strip().split(' ')
        exc[v_v[0]] = v_v[1]
    return exc

noun = sorted(set(read_wn_data_words('./words_data/data.noun')))
verb = sorted(set(read_wn_data_words('./words_data/data.verb')))
nouns_exc = read_wn_exc('./words_data/noun.exc')
verbs_exc = read_wn_exc('./words_data/verb.exc')

save_json(noun, './words_data/data.noun.wordsonly.json')
save_json(verb, './words_data/data.verb.wordsonly.json')
save_json(nouns_exc, './words_data/noun.exc.json')
save_json(verbs_exc, './words_data/verb.exc.json')