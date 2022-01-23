import contextlib, time, sys

UNIX_OS_OPTS = ["linux","linux2","darwin"]

class ElapsedTime(contextlib.ContextDecorator):
    ''' Measures the elapsed time
    '''
    def __init__(self, msg:str=None, print_on_exit=True):
        self.start = self.now()
        self.stop = None
        self.msg = msg
        self.print_on_exit = print_on_exit

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.stop = self.now()
        if self.print_on_exit:
            print('Time elapsed for {}: {}'.format(self.msg, self), file=sys.stderr)

    @staticmethod
    def now():
        if any( [ x in sys.platform for x in UNIX_OS_OPTS] ):
            return time.clock_gettime(time.CLOCK_MONOTONIC)
        elif sys.platform == "win32":
            return time.monotonic()
        raise BaseException("Could not determine OS.")

    @property
    def interval(self):
        return (self.stop - self.start) # seconds

    def __str__(self):
        return '{:0.06f} seconds'.format(self.interval)