#!/usr/bin/env python
''' Script to disable throttling on unix CPUs '''
from __future__ import with_statement

from subprocess import call, Popen, PIPE


def get_n_cpus():
    n = 0
    with open('/proc/cpuinfo') as fobj:
        for line in fobj:
            if line.startswith('processor	:'):
                n += 1
    return n


def disable_throttling(processor_number):
    # disable throttling on available CPUs
    retcode = call('cpufreq-selector -g performance -c %d' % processor_number, shell=True)
    if retcode:
        raise OSError('Apparently failed to set cpu frequency - '
                      'do you need to run this script as root?')


def main():
    for pno in range(get_n_cpus()):
        disable_throttling(pno)


if __name__ == '__main__':
    main()
