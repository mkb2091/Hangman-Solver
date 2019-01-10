import glob
import re

def suggest_next(words, string, not_in='', letters='abcdefghijklmnopqrstuvwxyz'):
    length = len(string)
    blank = '[%s]' % ''.join(l for l in letters if l not in not_in + string)
    regex = ''.join(re.escape(i) if i != '_' else blank for i in string)
    regex = re.compile(regex)
    counts = dict((i, 0) for i in letters if i not in not_in)
    for word in words:
        if len(word) == length:
            if regex.fullmatch(word):
                for l in set(word):
                    counts[l] += 1
    counts = [(counts[i], i) for i in counts if i not in string]
    return sorted(counts, reverse=True)


def clean(letters='abcdefghijklmnopqrstuvwxyz'):
    for path in glob.glob('wordlists/*.txt'):
        print('Opening', path)
        with open(path, 'rb') as file:
            words = file.read().decode('utf-8', 'ignore').lower().splitlines()
        base_length = len(words)
        words = [word for word in set(words) if all(l in letters for l in word)]
        print('Writing, old %s, new %s' % (base_length, len(words)))
        with open(path, 'w') as file:
            file.write('\n'.join(words))

def build(letters='abcdefghijklmnopqrstuvwxyz'):
    words = []
    for path in glob.glob('wordlists/*.txt'):
        print('Opening', path)
        with open(path) as file:
            words.extend(file.read().lower().splitlines())
    base_length = len(words)
    words = [word for word in words if all(l in letters for l in word)]
    words.sort()
    print('Writing, old %s, new %s' % (base_length, len(words)))
    with open('wordlist.txt', 'w') as file:
        file.write('\n'.join(words))
def main():
    words = []
    for path in glob.glob('*.txt'):
        print('Opening', path)
        with open(path) as file:
            words.extend(file.read().lower().splitlines())
    while True:
        string = input('String>>>')
        not_in = input('Letters not in>>>>')
        print('\n'.join('%s %s' % i for i in suggest_next(words, string, not_in)))
        

if __name__ == '__main__':
    main()
