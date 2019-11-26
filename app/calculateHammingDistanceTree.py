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
        
def hammingDistanceTree(tsvfile, out, prefix, transpose, boot):
  inputpath = tsvfile
  treespath = os.path.join(out,"trees")
  checkexists(treespath)

  # setup command
  cmd = f'bash -c \"hammingDistanceTree.py {inputpath} /output/ {transpose} {boot}\"'

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write(f'Calculating hamming distance tree and boostrapping {boot} times\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{inputpath:"/data",treespath:"/output"})
      outlog.write('***********\n')

def consensusTree(out):
  inputpath = os.path.join(out,"trees")
  consensuspath = os.path.join(out,"consensus")
  checkexists(consensuspath)

  # setup command
  cmd = f'bash -c \"sumtrees.py -s consensus -o /output/mrc95.tree -f0.95 --p --d0 /data/bootstrapped_nj_trees.newick\"'

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating 95% majority rule consensus tree\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{inputpath:"/data",consensuspath:"/output"})
      outlog.write('***********\n')

def boostrapSupport(out)
  inputtrees = os.path.join(out,"trees")
  inputconsensus = os.path.join(out,"consensus")
  supportpath = os.path.join(out,"bootstrapSupport")
  checkexists(supportpath)

  # setup command
  cmd = f'bash -c \"sumtrees.py -d0 -p -o /output/mrc95_boostrapSupport.tree -t /data/mrc95.tree /data/bootstrapped_nj_trees.newick\"'
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating support for nodes in the consensus tree\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{inputtrees:inputconsensus:"/data",supportpath:"/output"})
      outlog.write('***********\n')
        
# ------------------------------------------------------

def calculateHammingDistanceTree(tsvfile, out, transpose, boot):
    hammingDistanceTree(tsvfile, out, transpose, boot)
    if boot != 0:
        consensusTree(out)
        boostrapSupport(out)
    if boot == 0:
        continue
