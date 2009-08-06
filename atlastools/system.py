import os
from functools import partial
from subprocess import check_call, Popen, PIPE

caller = partial(check_call, shell=True)


def make_targets(build_dir, targets=('all',)):
    pwd = os.getcwd()
    try:
        os.chdir(build_dir)
        for target in targets:
            caller('make ' + target)
    finally:
        os.chdir(pwd)





