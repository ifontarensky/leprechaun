#############
Leprechaun.py
#############
A simple rainbow table generator written in Python.

********
Synopsis
********
Leprechaun.py is a simple Python script used for generating cryptographic
rainbow tables. This script can compute hashes using the MD5, SHA1, SHA256 and
SHA512 algorithms. Leprechaun.py computes hashes from a given wordlist,
optionally appending any number of numerical digits to the word before computing
the hash.

*****
Usage
*****
    ``leprechaun.py [-h] [-w WORDLIST] [-o OUTPUT] [-n NUMBER] [-m] [-s] [-s2] [-s5]``
    
    optional arguments:
        -h, --help
            show this help message and exit
        -w WORDLIST, --wordlist WORDLIST
            The wordlist to hash (default=wordlist.txt)
        -o OUTPUT, --output OUTPUT
            Name of the rainbow table file (default=rainbow-table.txt)
        -n NUMBER, --number NUMBER
            Number of integers to append to end of password string (default=0)
        -m, --md5
            Generate MD5 hashes of given passwords (default)
        -s, --sha1
            Generate SHA1 hashes of given passwords
        -s2, --sha256
            Generate SHA256 hashes of given passwords
        -s5, --sha512
            Generate SHA512 hashes of given passwords

********
Examples
********
* Generate MD5 hashes from the included wordlist, without appending digits:

``python leprechaun.py``

* Generate SHA1 hashes from the included wordlist, without appending digits:

``python leprechaun.py -s``

* Generate SHA1 hashes from your own wordlist, appending 2 digits, outputting to your own rainbow table:

``python leprechaun.py -s -n 2 -w your-wordlist.txt -o your-rainbow-table.txt``

*******
License
*******
    The MIT License (MIT)

    Copyright (c) 2013 Zach Dziura

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
