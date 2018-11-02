from logging import info
from threading import Thread
from subprocess import Popen, PIPE, STDOUT


def find(collection, item, field='name'):
    """
    Finds an element in a collection which has a field equal
    to particular item value

    Parameters
    ----------
    collection : Set
        Collection of objects
    item
        value of the item that we are looking for
    field : string
        Name of the field from the object to inspect

    Returns
    -------
    object
        Corresponding element that has a field matching item in
        the collection
    """
    for s in collection:
        if s[field] == item:
            return s
    return None


def copy_replace(src, dst, pattern='', replace_value=''):
    """
    Copies a file from src to dst replacing pattern by replace_value

    Parameters
    ----------
    src : string
        Path to the source filename to copy from
    dst : string
        Path to the output filename to copy to
    pattern : string
        Pattern to replace inside the src file
    replace_value
        Value to replace by in the dst file

    """
    f1 = open(src, 'r')
    f2 = open(dst, 'w')
    for line in f1:
        f2.write(line.replace(pattern, replace_value))
    f1.close()
    f2.close()


def log_info(pipe):
    """ Default logging function """
    for line in iter(pipe.readline, b''):
        info(line)
    return True


class BackgroundThreadRunner(object):
    """
    Worker Thread to run logging output in the background

    ...

    Attributes
    ----------
    process :
        Process object of the command running in the background
    log_function : function(stream -> bool)
        callback function to log the output of the command
    worker : Thread
        Thread object
    """
    def __init__(self, command, log_function):
        self.process = Popen(command, stdout=PIPE, stderr=STDOUT)
        self.log_function = log_function
        self.worker = Thread(name='worker', target=self.run)
        self.worker.start()

    def run(self):
        self.log_function(self.process.stdout)


def subprocess_run(command, log_function=log_info, wait=True):
    """
    Run command in a subprocess while redirecting output to log_function.

    The subprocess either runs synchroneoulsy or in the background depending on
    the wait parameter.

    Parameters
    ----------
    command : List
        Command to run in the subprocess
    log_function : function
        Callback function to log the output of the subprocess
    wait : bool
        Whether the subprocess should be run synchroneously or in
        the background
    Returns
    -------
    int
        return code of the subprocess
    BackgroundThreadRunner
        the thread running in the background
    """
    if wait:
        process = Popen(command, stdout=PIPE, stderr=STDOUT)
        with process.stdout:
            log_function(process.stdout)
        return process.wait()
    else:
        return BackgroundThreadRunner(command, log_function)