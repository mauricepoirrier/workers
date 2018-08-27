import os
import sys

from queue import Queue
from threading import Thread
import pandas as pd

NUM_THREAD = 2
DELAY = 1

def executer(i,q):
    '''
    Function that execute the python script by a Queue
    Edited to execute scraper.py for example
    '''
    while True:
        author_id = q.get()
        os.system("python scraper.py {}".format(author_id))
        q.task_done()

def reader(NAME_FILE):
    return pd.read_csv(NAME_FILE)

def fill_queue(q):
    '''
    Fill queue by a CSV file given in the command line
    Edited by an a specific column on the df
    '''
    df =  reader(sys.argv[1])

    for i in range(len(df)):
        q.put(df.iloc[i]['Scholar_id'])
    return q

def main():
    '''
    Main function by the command line and execution of Threads
    '''
    THE_QUEUE = Queue()

    for i in range(NUM_THREAD):
        worker = Thread(target=executer,args=(i,THE_QUEUE))
        worker.setDaemon(True)
        worker.start()

    THE_QUEUE = fill_queue(THE_QUEUE)

    THE_QUEUE.join()

if __name__ == '__main__':
    sys.exit(main())
