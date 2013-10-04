#!/usr/bin/env python3
import json, sys, time, random, subprocess, blessings, progressbar, concurrent.futures

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
    #for i in range(100):
    #    time.sleep(random.random() / 50)
    #    pbar.update(i)
    
    for line in subprocess.Popen(json.loads(kwargs["cmd"]), stdout=subprocess.PIPE).stdout:
        pbar.update(int(line))
    pbar.finish()

def test_parallel():
    with term.fullscreen():
        with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
            executor.map(test, [{"location":(0, num), "cmd": arg} for num,arg in enumerate(sys.argv[1:])])

if __name__ == '__main__':
    test_parallel()
