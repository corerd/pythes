'''Hunspell Thesaurus Class

Hunspell is a spell checker.
- Home page: http://hunspell.github.io

PyThes is a Python port of C++ MyThes class, whose project page is:
- https://github.com/hunspell/mythes

PyThes class uses Hunspell structured thesaurus data files
whose description can be found in the original project repository:
- https://github.com/hunspell/mythes/blob/master/data_layout.txt

Thesaurus files are bundled in LibreOffice / OpenOffice Language Packs
together spellchecking and hyphenation dictionaries used for stemming
and morphological generation.

The root name of thesaurus files is prefixed by th_ following Language
and Country Code, more an optional suffix, e.g.:

th_en_US_v2.dat th_en_US_v2.idx
th_it_IT_v2.dat th_it_IT_v2.idx

LibreOffice language bundles
----------------------------
- https://cgit.freedesktop.org/libreoffice/dictionaries/tree/
- https://wiki.documentfoundation.org/Language_support_of_LibreOffice
- https://github.com/LibreOffice/dictionaries

Language bundles are deployed in a single .oxt compressed file.
If your archive manager doesn't open .oxt file, then rename it as .zip
and there you have it.

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
https://github.com/corerd/pythes

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
from os.path import abspath, splitext, isfile
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


class ExcPyThes(Exception):
    '''Generic exception'''
    pass


class ExcIndexLinesCount(ExcPyThes):
    '''Read line count doesn't match with expected'''
    pass


class ExcLookupMissmatch(ExcPyThes):
    '''Entry found at byte offset into data file does not match lookup word'''
    pass


class PyThes:

    def __init__(self, thes_filepath):
        '''Gets from thes_filepath the thesaurus files names
        and loads the index file content as a dictionary of pairs
        { entry: byte_offset_into_data_file }

        thes_filepath can be:
            - root name of files
            - path to the thesaurus index file
            - path to the thesaurus data file
        '''
        self.idx_path, self.dat_path = self.get_filenames(thes_filepath)
        self.dat_encoding = self.get_encoding(self.dat_path)
        if self.idx_path == '':
            self.index = self.load_index_from_dat(self.dat_path)
        else:
            self.index = self.load_index(self.idx_path)

    def getIndex(self):
        '''Returns the index dictionary'''
        return self.index

    def get_filenames(self, filepath):
        '''Returns the couple of index, data files names from filepath

        The thesaurus consist of two files:
            - an optional index file (".idx" extension)
            - the data file (".dat" extension)

        filepath can be:
            - root name of files (without extemsion)
            - path to the thesaurus index file
            - path to the thesaurus data file
        '''
        rootname, ext = splitext(filepath)
        if ext is '.idx':
            idx_path = filepath
            dat_path = rootname + '.dat'
        elif ext is '.dat':
            idx_path = rootname + '.idx'
            dat_path = filepath
        else:
            idx_path = rootname + '.idx'
            dat_path = rootname + '.dat'
        dat_path = abspath(dat_path)
        idx_path = abspath(idx_path)
        if isfile(idx_path) is not True:
            idx_path = ''
        return idx_path, dat_path

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
        word = word.lower()
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
            line = dat_f.readline()
            entry, num_mean = line.split('|')
            if entry.lower() != word:
                raise ExcLookupMissmatch('search "{}", get "{}"'.format(word, entry))
            num_mean = int(num_mean)

            # get each meaning
            for _ in range(num_mean):
                mean = dat_f.readline().rstrip('\n').split('|')
                meanings += (Mean(mean[0], mean[1], tuple(mean[2:])),)

        return ThesaurusEntry(word, meanings)

    def load_index_from_dat(self, dat_path):
        '''Returns a dictionary of pairs { entry: byte_offset_into_data_file }
        from the thesaurus data file
        '''
        word_idx = {}
        with open(dat_path, 'r', encoding=self.dat_encoding) as dat_f:
            dat_f.readline()  # skip first line (file encoding)
            entry_byte_offset = dat_f.tell()
            while True:
                line = dat_f.readline()
                if line == '':
                    # the end of the file has been reached
                    break
                entry, num_mean = line.split('|')
                word_idx[entry.lower()] = entry_byte_offset
                for _ in range(int(num_mean)):
                    dat_f.readline()  # skip description lines
                entry_byte_offset = dat_f.tell()
        return word_idx

    def load_index(self, idx_path):
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
                word_idx[word[0].lower()] = int(word[1])
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
    # TEST BENCH: check integrity of thesaurus data files
    # checking thesaurus data entry for each word in the index
    dictionaries = (
        '../dictionaries/en_US/th_en_US_v2',
        '../dictionaries/it_IT/th_it_IT_v2',
        '../dictionaries/ca_ES/dictionaries/th_ca_ES_v3'
    )
    for thesaurus in dictionaries:
        th = PyThes(thesaurus)
        print('Data file: {}'.format(th.dat_path))
        print('Index file: {}'.format(th.idx_path))
        print('Searching {} words...'.format(len(th.index)))
        for word in th.getIndex():
            th.lookup(word)
    print('Done!')
