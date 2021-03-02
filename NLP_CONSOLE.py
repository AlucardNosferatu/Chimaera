import nltk


# import os


# proxy = 'http://127.0.0.1:1080'
# os.environ['http_proxy'] = proxy
# os.environ['HTTP_PROXY'] = proxy
# os.environ['https_proxy'] = proxy
# os.environ['HTTPS_PROXY'] = proxy

def verify_format(text):
    result = nltk.pos_tag(nltk.word_tokenize(text))
    a = None
    b = None
    c = None
    matched = False
    if len(result) == 3:
        if result[0][1].startswith('NN') or result[0][1] == 'PRP':
            if result[1][1].startswith('VB'):
                if result[0][1].startswith('NN') or result[0][1] == 'PRP':
                    print('Matched!')
                    matched = True
                    a = result[0][0]
                    b = result[1][0]
                    c = result[2][0]
                else:
                    print('Target Node Mismatch!')
            else:
                print('Relationship Mismatch!')
        else:
            print('Source Node Mismatch!')
    else:
        print('Length Mismatch!')
    return matched, a, b, c
