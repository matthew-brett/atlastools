''' Tests for make file parsing '''

from StringIO import StringIO

from nose.tools import assert_true, assert_false, assert_equal, assert_raises

from atlastools.makeparse import (lineparse, ParseResult, variable_sub,
                                  ParseLines, ParseError,
                                  SubstitutionError)


def test_parse_result():
    yield assert_raises, TypeError, ParseResult, 1
    pr1 = ParseResult('name', 'contents')
    yield assert_equal, pr1.name, 'name'
    yield assert_equal, pr1.contents, 'contents'
    yield assert_equal, pr1.forward_refs, []
    pr2 = ParseResult('name', 'contents', ['var1'])
    yield assert_equal, pr2.forward_refs, ['var1']
    yield assert_true, pr1 == pr2
    yield assert_false, pr1 != pr2
    pr2.contents = None
    yield assert_false, pr1 == pr2
    yield assert_equal, str(pr1), 'name := contents'
    yield assert_equal, str(pr2), ''


def test_lineparse():
    null_parse = ParseResult(None, None)
    yield assert_equal, lineparse('# a comment'), null_parse
    yield assert_equal, lineparse('a comment'), null_parse
    yield assert_equal, lineparse(' VAR = 4'), null_parse
    yield assert_equal, lineparse('\tVAR = 4'), null_parse
    yield assert_equal, lineparse('VAR: = 4'), null_parse
    yield assert_equal, lineparse('VAR+ = 4'), null_parse
    yield assert_equal, lineparse('VAR? = 4'), null_parse
    yield assert_equal, lineparse('VAR+VAR2 = 4'), null_parse
    yield assert_equal, lineparse('VAR = 4'), ParseResult('VAR','4')
    yield assert_equal, lineparse('VAR := 4'), ParseResult('VAR','4')
    yield assert_equal, lineparse('VAR ?= 4'), ParseResult('VAR','4')
    yield assert_equal, lineparse('VAR += 4'), ParseResult('VAR','4')
    yield (assert_equal, lineparse('VAR += 4', {'VAR': '3'}),
           ParseResult('VAR','3 4'))
    yield (assert_raises, SubstitutionError, lineparse,
           'VAR2 = $(VAR1)')
    context = {'VAR1':'some string'}
    yield (assert_equal, lineparse('VAR2 = $(VAR1)', context),
           ParseResult('VAR2', 'some string'))
    in_str = 'var1 = a long variable \\  '
    yield assert_raises, ParseError, lineparse, in_str
    in_str = 'var1 = a long variable \\'
    yield assert_raises, ParseError, lineparse, in_str


def _str_sub(in_str, subs):
    in_stream = StringIO(in_str)
    out_stream = StringIO()
    variable_sub(in_stream, out_stream, subs)
    return out_stream.getvalue()

    
def test_variable_sub():
    in_str = '''
# comment
VAR1 = 3
VAR2 = 4
'''
    yield assert_equal, _str_sub(in_str,{}), in_str
    # test dictionary return
    in_stream = StringIO(in_str)
    out_stream = StringIO()
    context = variable_sub(in_stream, out_stream, {})
    yield assert_equal, context, {'VAR1': '3',
                                  'VAR2': '4'}
    out_str = '''
# comment
VAR1 := some string
VAR2 = 4
'''
    dct = {'VAR1':'some string'}
    yield assert_equal, _str_sub(in_str, dct), out_str
    
    
def test_parse_lines():
    pl = ParseLines()
    yield assert_equal, pl.context, {}
    res1 = pl.checked_parse('var1 = 3')
    yield assert_equal, pl.context, {'var1': '3'}
    res1 = pl.checked_parse('var2 = $(var1)')
    yield assert_equal, pl.context, {'var1': '3', 'var2': '3'}
    print pl._forward_refs
    yield assert_raises, SubstitutionError, pl.checked_parse, 'var1 = 4'
    # no error for simple reference case though
    res = pl.checked_parse('var3 = 3')
    res = pl.checked_parse('var4 := $(var3)')
    res = pl.checked_parse('var3 = 4')
    # or ? reference case
    res = pl.checked_parse('var5 := $(var3)')
    res = pl.checked_parse('var3 = 4')
    
