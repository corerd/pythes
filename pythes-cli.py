'''Search Hunspell thesaurus for words and related information
'''
import sys
from ntpath import basename
from pythes import PyThes


def display(word_meanings):
    print('LOOK UP:', word_meanings.word)
    print('{:8} | {:30} | {}'.format('POS', 'MEAN', 'SYNONYMS'))
    for meaning in word_meanings.mean_tuple:
        print('{:8} | {:30} | {}'
                .format( meaning.pos,
                         meaning.main,
                         '; '.join(meaning.syn_tuple)) )


def main(argv):
    if len(argv) != 3:
        print('SYNTAX: {} <path-to-thesaurus-files> <lookup-word>'
                                            .format(basename(argv[0])))
        return -1
    thes_filepath = argv[1]
    word_to_lookup = argv[2]
    try:
        th = PyThes(thes_filepath)
    except FileNotFoundError as e:
        print('ERROR: {}: "{}"'.format(e.strerror, e.filename))
        return -1
    meanings = th.lookup(word_to_lookup)
    if meanings is None:
        print('NOT FOUND: "{}"'.format(word_to_lookup))
        return -1
    display(meanings)
    return 0


if __name__ == "__main__":
    arguments = sys.argv
    exit(main(arguments))
