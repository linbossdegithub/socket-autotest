'''
Created on 2018.10.15
@author: chenyongfa
'''
import threading
import socket

# q = Queue.Queue()
class RecThread(threading.Thread):
    def __init__(self, queue=None,socket=None,key=None,group=None, target=None, name=None, 
        args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self.queue = queue
        self.socket = socket
        self.key = key
        self._stop = False


    def run(self):
        while True:
            try:
                data = self.socket.recv(1024)
            except socket.error,e:
                print e.message
                return
            if not data:
                # print self.key+"data wei kong le"
                return
            self.queue.put(data)
    def stop(self):
        self._stop=True    