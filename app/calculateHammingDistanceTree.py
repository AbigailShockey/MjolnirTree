#!/usr/bin/python3

import os,sys
import app.callDocker as cd
import subprocess as sub
import shlex

def checkexists(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        os.mkdir(path)
        return False
    else:
        return True

def hammingDistanceTree(tsvfile, out, transpose, boot):
  logfile = os.path.join(out,'hdt.log')
  inputpath = os.path.dirname(tsvfile)
  tsv = os.path.basename(tsvfile)
  distancepath = os.path.join(out,"hammingDistance")
  checkexists(distancepath)

  # setup command
  cmd = f'bash -c \"hammingDistanceTrees.py /data/{tsv} /output/ {transpose} {boot}\"'
  print(cmd)
  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write(f'Calculating hamming distance tree and boostrapping {boot} times\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{inputpath:"/data",distancepath:"/output"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {distancepath}/hamming_distance_matrix.tsv {out}")
  sub.Popen(cmd).wait()
  if boot != 0:
      cmd = shlex.split(f"cp {distancepath}/bootstrapped_nj_trees.newick {out}")
      sub.Popen(cmd).wait()



def consensusTree(out):
  logfile = os.path.join(out,'consensus.log')
  inputpath = os.path.join(out,"hammingDistance")
  consensuspath = os.path.join(out,"consensusTree")
  checkexists(consensuspath)

  # setup command
  cmd = f'bash -c \"sumtrees.py -s consensus -o /output/mrc95.tree -f0.95 --percentages --decimals=0 /data/bootstrapped_nj_trees.newick\"'

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating 95% majority rule consensus tree\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{inputpath:"/data",consensuspath:"/output"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {consensuspath}/mrc95.tree {out}")
  sub.Popen(cmd).wait()

def boostrapSupport(out):
  logfile = os.path.join(out,'support.log')
  supportpath = os.path.join(out,"bootstrapSupport")
  checkexists(supportpath)

  # setup command
  cmd = f'bash -c \"sumtrees.py --decimals=0 -p -o /output/mrc95_boostrapSupport.tree -t /data/mrc95.tree /data/bootstrapped_nj_trees.newick\"'
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating support for nodes in the consensus tree\n')
      results = cd.call('ashockey/mjolnir:latest',cmd,'/data',{out:"/data",supportpath:"/output"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {supportpath}/mrc95_boostrapSupport.tree {out}")
  sub.Popen(cmd).wait()

# ------------------------------------------------------

def calculateHammingDistanceTree(tsvfile, out, transpose, boot):
    hammingDistanceTree(tsvfile, out, transpose, boot)
    if boot != 0:
        consensusTree(out)
        boostrapSupport(out)
