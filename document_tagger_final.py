__author__ = 'Gil Mandler'


import re
import sys
import os


metadata_dic ={
    'title' : re.compile(r'(title:\s*)(?P<title>.*)', re.IGNORECASE),
    'author' : re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE),
    'translator' : re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE),
    'illustrator' : re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)
    } # dictionary of the metadata to search for with compiled patterns


def compile_kws(args):
    """
    :param args: words entered at commandline as args from [2:]
    :return: dictionary of words and their respective complied regex pattern
    """
    kws = {kw : re.compile(r'\b' + kw + r'\b') for kw in args}
    return kws


def metadata_search(contents):
    """
    :param contents: string before filtered by filter_body()
    :return: dictionary of metadata found in the string
    """
    results = {}
    for kw in metadata_dic.keys():
      match = re.search(metadata_dic[kw], contents)
      if match:
          results[kw] = match.group(kw)
    return results


def print_metadata(metadata, docname):
    """
    prints the results found in meta_data search()

    :param metadata: dictionary of words and their complied pattern
    :param docname: filename of the document that was searched

    :return: none
    """
    print
    print "***" * 25
    print "Here's the info for doc {}:".format(docname)
    for k in metadata.keys():
      temp = str(k).title()
      if k != 'title':
        temp += '(s)'
      print "{0}: {1}".format(temp, metadata[k])


def filter_body(contents):
    """
    :param contents: string
    :return: the string contents found between ***start*** and ***end***
    """
    split_doc = re.compile(r'(\*{3}START\*{3}\n)(?P<body>.*)(\n\*{3}END\*{2,})', re.DOTALL)
    body = split_doc.search(contents).group('body')
    return body


def keyword_search(docname, kws, contents):
    """
    prints results of the keywords search in the current docname

    :param docname: name of document being worked on
    :param kws: dictionary of keywords and their compiled regex patterns
    :param contents: string after run through filter_body

    :return:none
    """
    print
    print "Here's the keyword info for doc {}:".format(docname)
    for kw in kws.keys():
        print "\"{0}\": {1}".format(kw, len(re.findall(kws[kw], filter_body(contents))))



def create_docs(dir):
    """
    :param dir: absolute path to search for files
    :return: dictionary of text file names and their contents
    """
    documents = {}
    for file in os.listdir(dir):
        if file.endswith('.txt'):
            doc = os.path.join(dir, file)
            with open(doc, 'r') as f:
                contents = f.read()
            documents[file] = contents
    return documents


def reporter(documents, kws):
    """
    iterates over text files and processes them with helper functions

    :param documents: dictionary of text files and their contents
    :param kws: dictionary of words and their compiled regex pattern

    :return:none

    """
    for docname in documents.keys():
        metadata = metadata_search(documents[docname])
        print_metadata(metadata, docname)
        keyword_search(docname, kws, documents[docname])


def main():
    kws = compile_kws(sys.argv[2:])
    docs = create_docs(sys.argv[1])
    reporter(docs, kws)


if __name__ == '__main__':
    main()