'''
Created on 2018.10.16
@author: chenyongfa
'''
import threading
import time



class HeartThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self,socket=None,sn=None,heart_data=None,group=None, target=None, name=None, 
        args=(), kwargs=None, verbose=None):
        threading.Thread.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs, verbose=verbose)
        self.stop_event = False
        self.socket = socket
        self.sn = sn
        self.heart_data = heart_data

    def stop(self):
        self.stop_event=True
    
    def run(self):
        
        while True:
            for i in range(10):
                time.sleep(1)
                if self.stop_event:
                    return
            try:
                self.socket.sendall(self.heart_data)
            except:
                pass
                # print "heartbeat error"
            # print "heartbeat"


