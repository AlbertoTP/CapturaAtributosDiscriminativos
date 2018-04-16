# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 16:33:04 2018

@author: alternatif
"""

import threading
import time
import sys
import pp


dicPos={}
dicNeg={}
salida=""

class Thread(threading.Thread):
    def __init__(self, name, msm):
        threading.Thread.__init__(self)
        self.name = name
        self.msm=msm

    def run(self):
        global dicPos
        global dicNeg
        global salida
        salida+="1"
        cad = ">>> "+self.msm+ self.getName()+" "
        cad+=str(dicPos)
        cad+=str(dicNeg)
        cad+=salida
        print cad
        #time.sleep(5)



#a = Thread("myThread_name_A")
#b = Thread("myThread_name_B")
#c = Thread("myThread_name_C")
#
#a.start()
#b.start()
#c.start()
#
#a.join()
#b.join()
#c.join()

# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"


for i in range(0,job_server.get_ncpus()):
    print "hilo"
    Thread("myThread_name_"+str(i),"hola").start()