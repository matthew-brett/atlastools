''' Simple make file variable set line parsing, writing

Meaning, only intended to read and write lines of form:

MYVARIABLE = some value

or

MYVARIABLE := some value

http://www.gnu.org/software/make/manual/make.html#Setting

`` = `` gives recursively expanded
`` := `` gives simply expanded
`` ?= `` means define if not set

For now we only deal fully with simple expansion, or recursive expansion
that only makes backward references.  That is, if you have something
like this::

   var1 = $(var2)
   var2 = something

then we'll raise an error. But, if you have::

   var1 = something
   var2 = $(var2)

then we'll let you through.

There's also a '+=' command for appending text; this we do handle.

There is a ``define`` directive:

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
    def __init__(self, name, contents, message=None, forward_refs=None):
        self.name = name
        self.contents = contents
        self.message = message
        if forward_refs is None:
            forward_refs = []
        self.forward_refs = forward_refs
        
    def __eq__(self, other):
        return (self.name == other.name and
                self.contents == other.contents)

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        if self.contents is None:
            return ''
        return '%s := %s' % (self.name, self.contents)


def lineparse(line, context=None):
    ''' Return possible variable contents from Makefile line

    Use dict `context` to do any variable replacement for variables
    in dict.
    '''
    if context is None:
        context = {}
    message = None
    forward_refs = []
    match = var_re.match(line)
    if not match:
        return ParseResult(None, None)
    name, modifier, contents = match.groups()
    contents = contents.strip()
    if modifier == '+':
        if name in context:
            contents = '%s %s' % (context[name], contents)
    sub_matches = list(varsub_re.finditer(contents))
    if sub_matches:
        if modifier == '': # recursive substitution -> forward refs
            for smatch in sub_matches:
                mstr = smatch.groups()[0][1:-1]
                forward_refs.append(mstr)
        sub_contents = varsub_re.sub(r'%\1s', contents)
        try:
            contents = sub_contents % context
        except KeyError:
            return ParseResult(
                name,
                None,
                'Failed variable substitution for "%s"' % contents)
    return ParseResult(name, contents, message, forward_refs)


class ParseLines(object):
    ''' Class to keep context of Makefile parse

    Used to keep variables for variable substitution, and raise errors
    when we find redefinition of variables that we have already used in
    recursive substitution.

    Note that the `context` input dictionary will be modified parsing
    lines, so you may want to copy it before passing into the
    constructor. 
    '''
    def __init__(self, context=None):
        if context is None:
            context = {}
        self.context = context
        self._forward_refs = []
        
    def checked_parse(self, line):
        parse_result = lineparse(line, self.context)
        name, contents = parse_result.name, parse_result.contents
        if name in self._forward_refs:
            raise MakeParseError('Detected changed forward reference')
        self._forward_refs += parse_result.forward_refs
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
            contents = substitutions[name]
            line = '%s := %s\n' % (name, substitutions[name])
        if not contents is None:
            context[name] = contents
        out_stream.write(line)
    return pl.context       
