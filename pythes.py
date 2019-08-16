'''Hunspell Thesaurus Class

Hunspell is a spell checker.
- Home page: http://hunspell.github.io

PyThes is a Python port of C++ MyThes class, whose project page is:
- https://github.com/hunspell/mythes

PyThes class uses Hunspell structured thesaurus data files
whose description can be found in the original project repository:
- https://github.com/hunspell/mythes/blob/master/data_layout.txt
A copy of such file is also available in this repository.

Disclaimer
----------
The author of this software is not affiliated, associated, authorized,
endorsed by, or in any way officially connected with any of the companies,
organizations and individuals mentioned above.

None of them can be hold liable for any damages arising out of the use
of this software.

MIT License
---------------
Copyright (c) 2019 Corrado Ubezio

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from collections import namedtuple


# The thesaurus entry of a word consists of:
# word       - the word itself
# mean_tuple - the means related to the word
ThesaurusEntry = namedtuple('ThesaurusEntry', 'word mean_tuple')

# each mean consists of:
# pos       - part of speech or other meaning specific description
# main      - main mean
# syn_tuple - the synonyms related to the mean
Mean = namedtuple('Mean', 'pos main syn_tuple')


class ExcIndexLinesCount(Exception):
    '''Read line count doesn't match with expected'''
    pass


class ExcLookupMissmatch(Exception):
    '''Entry found at byte offset into data file does not match lookup word'''
    pass


class PyThes:

    def __init__(self, idx_path, dat_path):
        '''Get thesaurus index and data files'''
        self.index = self.get_index(idx_path)
        self.dat_encoding = self.get_encoding(dat_path)
        self.dat_path = dat_path

    def lookup(self, word):
        '''Returns ThesaurusEntry namedtuple related to the word
        fetched from thesaurus data file.

        Thesaurus data is a text file with the following lines content:
            Line 1: a string describes the encoding subsequently used.

            All of the remaning lines of the file follow this structure:
                entry|num_mean
                pos|syn1_mean|syn2|...
                .
                .
                .
                pos|mean_syn1|syn2|...
                        
            where:
                entry    - lowercase version of the word or phrase being described
                num_mean - number of meanings for this entry
            
            There is one meaning per line and each meaning is comprised of:
                pos       - part of speech or other meaning specific description
                syn1_mean - synonym 1 also used to describe the meaning itself 
                syn2      - synonym 2 for that meaning etc.
        '''
        try:
            # find word in the index
            offset_into_dat = self.index[word]
        except KeyError:
            # not found
            return None

        meanings = ()
        with open(self.dat_path, 'r', encoding=self.dat_encoding) as dat_f:
            dat_f.seek(offset_into_dat)

            # grab entry and count of the number of meanings
            entry, num_mean = dat_f.readline().split('|')
            if entry != word:
                raise ExcLookupMissmatch()
            num_mean = int(num_mean)

            # get each meaning
            for _ in range(num_mean):
                mean = dat_f.readline().rstrip('\n').split('|')
                meanings += (Mean(mean[0], mean[1], tuple(mean[2:])),)

        return ThesaurusEntry(word, meanings)

    def get_index(self, idx_path):
        '''Returns the thesaurus index file content as a dictionary of pairs
        { entry: byte_offset_into_data_file }

        Thesaurus index is a text file with the following lines content:
            Line 1: a string describes the encoding subsequently used;
            Line 2: a count of the total number of entries in the thesaurus.

            All of the remaining lines are of the form:
                entry|byte_offset_into_data_file_where_entry_is_found
        '''
        word_idx = {}
        idx_codec = self.get_encoding(idx_path)
        with open(idx_path, 'r', encoding=idx_codec) as idx_f:
            idx_f.readline()  # skip first line (file encoding)
            idx_size = int(idx_f.readline())
            cnt = 0  # now parse the remaining lines of the index
            for line in idx_f:
                word = line.split('|')
                word_idx[word[0]] = int(word[1])
                cnt += 1
            if idx_size != cnt:
                raise ExcIndexLinesCount()
        return word_idx

    def get_encoding(self, thesaurus_file):
        '''Returns first line of thesaurus_file as encoding type.

        thesaurus_file is a text file where line 1 describes the encoding used.
        This function opens the source text file in encoding-agnostic mode,
        that is binary, to get the ASCII string revealing the encoding type
        that will be later used to re-open the thesaurus_file in text mode.
        '''
        with open(thesaurus_file, 'rb') as f:
            # convert first binary line to string, removing trailing newline
            encoding_type = f.readline().decode('ascii').rstrip('\n')
        return encoding_type


if __name__ == "__main__":
    # Paths are relative to VsCode workspace folder
    th = PyThes('dict-it/dictionaries/th_it_IT_v2.idx',
                'dict-it/dictionaries/th_it_IT_v2.dat')

    # Verify that there is a thesaurus entry for each word in the index
    print('Searching {} words...'.format(len(th.index)))
    for word in th.index:
        th.lookup(word)
    print('Done!')
