import sys
import json

def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

nouns = read_json('./words_data/data.noun.wordsonly.json')
verbs = read_json('./words_data/data.verb.wordsonly.json')
nouns_exc = read_json('./words_data/noun.exc.json')
verbs_exc = read_json('./words_data/verb.exc.json')

def base_form(word):
    word = word.lower()

    for lst in [nouns, verbs]:
        if word in lst:
            return word
    for dct in [nouns_exc,verbs_exc]:
        if word in dct:
            return dct[word]

    rules = [
        [lambda w: w[-1:]=='s',lambda w: w[:-1]], # (verb|noun)-s
        [lambda w: w[-2:]=='es',lambda w: w[:-2]], # (verb|noun)-es
        [lambda w: w[-3:]=='ies',lambda w: w[:-3]+'y'], # (verb|noun)-ies
        # verb-ing
        [lambda w: w[-3:]=='ing',lambda w: w[:-3]],
        [lambda w: w[-3:]=='ing',lambda w: w[:-3]+'e'],
    ]
    for rule in rules:
        if rule[0](word):
            base = rule[1](word)
            if base in nouns or base in verbs:
                return base
    return word

def filter_words(text):
    alphabet = [
        'A','a','B','b','C','c','D','d','E','e','F','f','G','g','H','h','I','i','J','j','K','k','L','l','M','m','N','n','O','o','P','p','Q','q','R','r','S','s','T','t','U','u','V','v','W','w','X','x','Y','y','Z','z'
    ]
    words = []
    idx = 0
    while idx < len(text):
        if text[idx] in alphabet:
            length = 1
            while ( 
                idx+length < len(text)
                and (
                    text[idx+length] in alphabet 
                    or (idx+length+1 < len(text) and text[idx+length] in ['\'','-','’'] and text[idx+length+1] in alphabet))
                ):
                length += 1

            words.append(text[idx:idx+length])
            idx += length+1
        else:
            idx += 1
    return words

def count_words(words):
    '''
    {
        'base': {
            'appearance': {
                'form_1': times
            }
            'total': times
        }
    }
    '''
    res = {}
    for word in words:
        base = base_form(word)
        if base not in res:
            res[base] = {
                'appearance':{},
                'total':0
            }
        if word not in res[base]['appearance']:
            res[base]['appearance'][word] = 0
        res[base]['total'] += 1
        res[base]['appearance'][word] += 1
    return res

if __name__ == "__main__":
    try:
        with open(sys.argv[-1], 'r') as f:
            words = filter_words(f.read())
    except UnicodeDecodeError:
        with open(sys.argv[-1], 'r', encoding='utf-8') as f:
            words = filter_words(f.read())
    
    wc = count_words(words)
    lst = [(k,wc[k]) for k in wc]
    lst.sort(key=lambda item: item[1]['total'],reverse=True)
    with open('result.csv', 'w', encoding='gbk') as f:
        f.write('"单词","出现形式","出现次数"\n')
        for item in lst:
            f.write(f'"{item[0]}",')
            f.write('"'+', '.join([f'{w}({item[1]["appearance"][w]})' for w in item[1]['appearance']])+'",')
            f.write(f'{item[1]["total"]}\n')
