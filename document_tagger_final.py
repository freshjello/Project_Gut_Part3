__author__ = 'Gil Mandler'


import re
import sys
import os

title_search = re.compile(r'(title:\s*)(?P<title>.*\n.*)', re.IGNORECASE)
author_search = re.compile(r'(author:)(?P<author>.*)', re.IGNORECASE)
translator_search = re.compile(r'(translator:)(?P<translator>.*)', re.IGNORECASE)
illustrator_search = re.compile(r'(illustrator:)(?P<illustrator>.*)', re.IGNORECASE)


def compile_kws(args):
    kws = {kw : re.compile(r'\b' + kw + r'\b') for kw in args}
    return kws


def filter_body(contents):
    split_doc = re.compile(r'(\*{3}START\*{3}\n)(?P<body>.*)(\n\*{3}END\*{2,})', re.DOTALL)
    body = split_doc.search(contents).group('body')
    return body


def metadata_search(contents):
      metadata ={}
      metadata['title'] = re.search(title_search, contents).group('title')
      author = re.search(author_search, contents)
      translator = re.search(translator_search, contents)
      illustrator = re.search(illustrator_search, contents)
      if author:
        metadata['author'] = author.group('author')
      else:
        metadata['author'] = ''
      if translator:
        metadata['translator'] = translator.group('translator')
      else:
        metadata['translator'] = ''
      if illustrator:
        metadata['illustrator'] = illustrator.group('illustrator')
      else:
        metadata['illustrator'] = ''
      return metadata


def print_metadata(metadata, docname):
      print "***" * 25
      print "Here's the info for doc {}:".format(docname)
      print "Title: {}".format(metadata['title'])
      print "Author(s): {}".format(metadata['author'])
      print "Translator(s): {}".format(metadata['translator'])
      print "Illustrator(s): {}".format(metadata['illustrator'])
      print "\n"


def keyword_search(docname, kws, contents):
      print "***" * 25
      print "Here's the keyword info for doc {}:".format(docname)
      for kw in kws.keys():
        print "\"{0}\": {1}".format(kw, len(re.findall(kws[kw], filter_body(contents))))



def create_docs(dir):
    documents = {}
    for file in os.listdir(dir):
        if file.endswith('.txt'):
            doc = os.path.join(dir, file)
            with open(doc, 'r') as f:
                contents = f.read()
            documents[file] = contents
    return documents

def reporter(documents, kws):
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