Hunspell Thesaurus Support in Python
===================================
[Hunspell](http://hunspell.github.io/) is the spell checker of LibreOffice,
OpenOffice, Mozilla Firefox 3 & Thunderbird, Google Chrome,
and it is also used by proprietary software packages, like macOS, InDesign,
memoQ, Opera and SDL Trados.

**PyThes** is a Python class providing methods to search Hunspell thesaurus
for words and related information on part of speech, meanings and synonyms.

**PyThes-cli** is simple example script that looks up a word and returns
its meaning and synonyms.

Hunspell thesaurus consists of a `.dat` structured text data file
and an optional `.idx` index file.
You can find their description in the `data_layout.txt` file.

The root name of LibreOffice / OpenOffice thesaurus files is prefixed by `th_`
following Language and Country Code, more an optional suffix, e.g.:
```
th_en_US_v2.dat th_en_US_v2.idx
th_it_IT_v2.dat th_it_IT_v2.idx
```

Using the example script to look up an italian word, open a command line window
and enter only the thesaurus root name (without extensions) as follows: 
```
python pythes-cli.py directory-path-to/th_it_IT_v2 lookup-word
```
The script will open the `th_it_IT_v2.dat` and `th_it_IT_v2.idx` files
in the directory path.


How to get Hunspell thesaurus files
-----------------------------------
Thesaurus files are bundled in LibreOffice / OpenOffice Language Packs
together spellchecking and hyphenation dictionaries used for stemming
and morphological generation.

Goto to [Document Foundation Language/Support](https://wiki.documentfoundation.org/Language_support_of_LibreOffice)
and search for you language.

Language bundles are deployed as a single `.oxt` compressed file.

You can use an archive manager like 7-Zip to open the bundle and extract
the thesaurus file `.dat` and `.idx`.

If your archive manager doesn't recognize `.oxt` file, then rename it as `.zip`
and there you have it.

In the following web pages you can find the `.dat` files only:
- https://cgit.freedesktop.org/libreoffice/dictionaries/tree/
- https://github.com/LibreOffice/dictionaries


Other dictionaries
------------------
words (Unix) words is a standard file on Unix and Unix-like operating systems,
and is simply a newline-delimited list of dictionary english words.

The words file is usually stored in `/usr/share/dict/words` or `/usr/dict/words`.


Credits
-------
**PyThes** is a Python port of **C++ MyThes** class, whose project page is:
- https://github.com/hunspell/mythes


Disclaimer
----------
The author of this software is not affiliated, associated, authorized,
endorsed by, or in any way officially connected with any of the companies,
organizations and individuals mentioned above.

None of them can be hold liable for any damages arising out of the use
of this software.


MIT License
-----------
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
