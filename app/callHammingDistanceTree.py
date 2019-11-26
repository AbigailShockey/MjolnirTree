#!/usr/bin/env python 3

import os,sys
import app.callDocker as cd

def checkexists(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        os.mkdir(path)
        return False
    else:
        return True
        
def callHammingDistanceTree(tsvfile, out, prefix, transpose, boot):
    logfile = os.path.join(out,'mjolnir.log')
    resultspath = os.path.join(out,"results")
    checkexists(resultspath)
    # setup command
    cmd = f'bash -c \"hammingDistanceTree.py {tsv} {prefix} {transpose} {boot}\"'
    # denote logs
    with open(logfile,'a') as outlog:
        outlog.write('***********\n')
        outlog.write('Calculating hamming distance matrix and tree\n')
        results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{outdir:"/data"})
        outlog.write('***********\n')
