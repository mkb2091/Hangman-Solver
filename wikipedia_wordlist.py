import xml.etree.ElementTree as ET
import collections
import re
import os

def get_articles(path):
    tag_regex = re.compile('{.*?}(.*)')
    title = ''
    text = ''
    for event, elem in ET.iterparse(path, events=('end', )):
        tag = tag_regex.match(elem.tag).group(1)
        if tag == 'page':
            if '#REDIRECT' not in text:
                yield title, text
            title = ''
            text = ''
        elif tag == 'title':
            title = elem.text
        elif tag == 'text':
            if elem.text:
                text += elem.text
        elem.clear()

def get_meta(article):
    meta = {}
    for key, item in re.findall('|(\w+) = (\w+)', article):
        meta[key] = item
    return meta

def word_count(path, frequency=100):
    words = collections.Counter()
    position = 0
    word_regex = re.compile('(?:(?<=^)|(?<=\s))([A-Za-z]+)(?:(?=$)|(?=\s))')
    for title, text in get_articles(path):
        position += 1
        words.update(word_regex.findall(text))
        if position % frequency == 0:
            print('Position:', position, 'Words:', len(words))
            yield words


def save_word_wordcount(path, frequency=100):
    for current_result in word_count(path, frequency):
        try:
            result = current_result.most_common()
            with open('temp.txt', 'w') as file:
                file.writelines('%s,%s\n' % i for i in result)
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
    save_word_wordcount(path, 200)
