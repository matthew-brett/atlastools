#!/usr/bin/env python
''' Script to disable throttling on unix CPUs '''
from __future__ import with_statement

from subprocess import call, Popen, PIPE
import re


def n_processors():
    
    proc_re = re.compile(r'processor\W+:\W+(\d+)')
    max_pno = None
    with open('/proc/cpuinfo', 'rt') as cpuinfo:
        for line in cpuinfo:
            match = proc_re.match(line)
            if match:
                pno = int(match.groups()[0])
                if max_pno is None or pno > max_pno:
                    max_pno = pno
    if max_pno is None:
        return None
    return max_pno + 1


def disable_throttling(processor_number):
    # disable throttling on available CPUs
    retcode = call('cpufreq-selector -g performance -c %d' % processor_number, shell=True)
    if retcode:
        raise OSError('Apparently failed to set cpu frequency - '
                      'do you need to run this script as root?')


def main():
    n = n_processors()
    for pno in range(n):
        disable_throttling(pno)


if __name__ == '__main__':
    main()
