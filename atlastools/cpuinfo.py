''' Parse CPU info file returning dict

Obviously this is linux specific
'''
from __future__ import with_statement

import re

proc_re = re.compile(r'([\w\s]+\b)\s+:\s+(.*)')

converters = (
    int,
    float,
    str)


def get_cpuinfo():
    entries = []
    current = {}
    with open('/proc/cpuinfo') as fobj:
        for line in fobj:
            match = proc_re.match(line)
            if not match:
                continue
            name, value = match.groups()
            if name == 'processor':
                entries.append({})
            value = value.strip()
            for converter in converters:
                try:
                    value = converter(value)
                except ValueError:
                    continue
                entries[-1][name] = value
                break
    return entries
