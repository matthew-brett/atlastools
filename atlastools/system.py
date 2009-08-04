from functools import partial
from subprocess import check_call, Popen, PIPE

caller = partial(check_call, shell=True)


