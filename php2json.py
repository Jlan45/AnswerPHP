#!/usr/bin/env python

# php2json.py - Converts PHP to a JSON-based abstract syntax tree
# Usage: php2json.py < input.php > output.json

import sys
from phply.phplex import lexer
from phply.phpparse import make_parser
import json

input = sys.stdin
output = sys.stdout
with_lineno = True

def export(items):
    result = []
    if items:
       for item in items:
           if hasattr(item, 'generic'):
               item = item.generic(with_lineno=with_lineno)
           result.append(item)
    return result
def php2json(input_file, output_file):
    parser = make_parser()
    json.dump(export(parser.parse(input_file,
                                        lexer=lexer,
                                        tracking=with_lineno)),
                    output_file, indent=2)
    output_file.write('\n')
