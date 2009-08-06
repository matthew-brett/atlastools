''' Simple make file variable set line parsing, writing

Meaning, only intended to read and write lines of form:

MYVARIABLE = some value

or

MYVARIABLE := some value

http://www.gnu.org/software/make/manual/make.html#Setting

`` = `` gives recursively expanded
`` := `` gives simply expanded
`` ?= `` means define if not set

For now we only deal with simple expansion.  That is, if you have
something like this::

   var1 = $(var2)
   var2 = something

then we'll raise an error. But, if you have::

   var1 = something
   var2 = $(var2)

then we'll let you through.

There's also a '+=' command for appending text.  Error again.

There is a also a ``define`` directive:

http://www.gnu.org/software/make/manual/make.html#Defining

that we don't deal with.

We also take a rather severe line on variable names.  The only ones we
allow are those containing only letters, numbers and underscores; see:

http://www.gnu.org/software/make/manual/make.html#Using-Variables
'''

import re

var_re = re.compile(r'(\w+)\s*([:+\?]*)=\s*(.*)')
varsub_re = re.compile(r'\$(\(\w+\))')


class MakeParseError(Exception):
    pass


class ParseResult(object):
    def __init__(self, name, contents, message=None, modifier=None):
        self.name = name
        self.contents = contents
        self.message = message
        self.modifier = modifier
        
    def __eq__(self, other):
        return (self.name == other.name and
                self.contents == other.contents)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        if self.contents is None:
            return ''
        return '%s := %s' % (self.name, self.contents)


def lineparse(line, good_context=None):
    ''' Return possibe variable contents from Makefile line

    Use dict `good_context` to do any variable replacement for variables
    in dict.

    Use sequence `bad_names` to raise an error for variable substitution
    '''
    if good_context is None:
        good_context = {}
    message = None
    match = var_re.match(line)
    if not match:
        return ParseResult(None, None)
    name, modifier, contents = match.groups()
    contents = contents.strip()
    if modifier == '+':
        if name in good_context:
            contents = '%s %s' % (good_context[name], contents)
    if varsub_re.search(contents):
        sub_contents = varsub_re.sub(r'%\1s', contents)
        try:
            contents = sub_contents % good_context
        except KeyError:
            return ParseResult(
                name,
                None,
                'Failed variable substitution for "%s"' % contents)
    return ParseResult(name, contents, message, modifier)


class ParseLines(object):
    ''' Class to keep context of Makefile parse

    Used to keep variables for variable substition, and raise errors
    when we find redefinition of variables that we have already used in
    recursive substitution
    '''
    def __init__(self, context=None):
        if context is None:
            context = {}
        self.context = context
        self._rec_used_names = []
        
    def checked_parse(self, line):
        parse_result = lineparse(line, self.context)
        name, contents = parse_result.name, parse_result.contents
        if name in self._rec_used_names:
            raise MakeParseError('Detected unhandled back reference')
        if parse_result.modifier == '': # recursive substitution
            self._rec_used_names.append(name)
        if not contents is None:
            self.context[name] = contents
        return parse_result    


def variable_sub(in_stream, out_stream, substitutions, context=None):
    if context is None:
        context = {}
    pl = ParseLines(context)
    for line in in_stream:
        result = pl.checked_parse(line)
        name, contents = result.name, result.contents
        if name in substitutions:
            if contents is None:
                raise MakeParseError('Could not parse variable definition')
            line = '%s := %s\n' % (name, substitutions[name])
        if not contents is None:
            context[name] = contents
        out_stream.write(line)
    return pl.context       
