import xml.etree.ElementTree as ET
import collections
import re
import os

def get_articles(path):
    parser = ET.XMLPullParser(['start', 'end'])
    tag_regex = re.compile('{.*?}(.*)')
    with open(path, 'rb') as file:
        title = ''
        text = ''
        data = '1'
        while data:
            data = file.read(8192).decode('utf-8', 'ignore')
            parser.feed(data)
            for event, elem in parser.read_events():
                tag = tag_regex.match(elem.tag).group(1)
                if tag == 'page':
                    if event == 'end':
                        if '#REDIRECT' not in text:
                            yield title, text
                        title = ''
                        text = ''
                elif tag == 'title':
                    title = elem.text
                elif tag == 'text':
                    if elem.text and event=='end':
                        text += elem.text

def get_meta(article):
    meta = {}
    for key, item in re.findall('|(\w+) = (\w+)', article):
        meta[key] = item
    return meta

def word_count(path, frequency=100):
    words = collections.Counter()
    with open('wiki_words.txt') as file:
        old_words = dict(map(lambda x: x.split(','),
                         file.read().lower().splitlines()))
    for i in old_words:
        words[i] = int(old_words[i])
    position = int(input('Position>>>'))
    word_regex = re.compile('(?:(?<=^)|(?<=\s))([A-Za-z]+)(?:(?=$)|(?=\s))')
    for title, text in get_articles(path):
        position += 1
        words.update(word_regex.findall(text))
        
        
        if position % frequency == 0:
            print('Position:', position)
            yield words
                        

def save_word_wordcount(path, frequency=100):
    for current_result in word_count(path, frequency):
        try:
            result = current_result.most_common()
            with open('temp.txt', 'wb') as file:
                file.write('\n'.join('%s,%s' % i for i in result).encode())
            try:
                os.remove('wiki_words.txt')
            except FileNotFoundError:
                pass
            os.rename('temp.txt', 'wiki_words.txt')
        except Exception as error:
            print(error)

if __name__ == '__main__':
    path = (r'D:\Downloads\enwiki-20181020-pages-articles-multistream.xml'
            '\enwiki-20181020-pages-articles-multistream.xml')
    save_word_wordcount(path, 100)
