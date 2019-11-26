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
        
def callHammingDistanceTree(tsvfile, out, transpose, boot):
    treespath = os.path.join(out,"trees")
    checkexists(treespath)
    # setup command
    cmd = f'bash -c \"hammingDistanceTree.py {tsv} {transpose} {boot}\"'
    # denote logs
    with open(logfile,'a') as outlog:
        outlog.write('***********\n')
        outlog.write(f'Calculating hamming distance tree and boostrapping {boot} times\n')
        results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{out:"/data",treespath:"/output"})
        outlog.write('***********\n')

def consensusTree(out)
  inputpath = os.path.join(out,"trees")
  consensuspath = os.path.join(out,"consensus")
  checkexists(consensuspath)
  # setup command
  cmd = f'bash -c \"sumtrees.py -s consensus -o phylo-mle-support.sumtrees -f0.95 --p --d0 {inputpath}/bootstrapped_nj_trees.newick\"'
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating consensus tree\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{input_path:"/data",consensuspath:"/output"})
      outlog.write('***********\n')
