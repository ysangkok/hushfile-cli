#!/usr/bin/env python3
import json, sys, time, random, subprocess, blessings, progressbar, concurrent.futures, traceback

term = blessings.Terminal()

class Writer(object):
    def __init__(self, location):
        """ Input: location - tuple of ints (x, y), the position of the bar in the terminal """
        self.location = location

    def write(self, string):
        with term.location(*self.location):
            print(string)

def test(kwargs):
    """Input: location - tuple (x, y) defining the position on the screen of the progress bar """
    pbar = progressbar.ProgressBar(fd=Writer(kwargs["location"])) # fd is an object that has a .write() method
    pbar.start()
    
    p = subprocess.Popen([str(x) for x in json.loads(kwargs["cmd"])], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in p.stdout:
        pbar.update(int(line))
    pbar.finish()
    p.wait(timeout=5)
    if p.returncode != 0: raise Exception("return code: {}\nstdout: {}\nstderr: {}".format(p.returncode, p.stdout.decode("utf-8"), p.stderr.decode("utf-8")))

def test_parallel():
    with term.fullscreen():
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(test, {"location":(0, num), "cmd": arg}) for num,arg in enumerate(sys.argv[1:])]
            for future in futures:
                try:
                    future.result()
                except:
                    traceback.print_exc(file=sys.stderr)

if __name__ == '__main__':
    debug = False
    if debug:
        for i in sys.argv[1:]:
            print(i)
            p = subprocess.Popen([str(x) for x in json.loads(i)], stdout=subprocess.PIPE, bufsize=1)
            for line in iter(p.stdout.readline, b''):
                sys.stdout.buffer.write(line)
                sys.stdout.buffer.flush()
            p.communicate()
    else:
        test_parallel()
