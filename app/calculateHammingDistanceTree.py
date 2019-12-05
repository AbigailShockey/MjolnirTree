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
  cmd = f'bash -c \"hammingDistanceNJTrees.py /data/{tsv} /output/ {transpose} {boot}\"'

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write(f'Calculating hamming distance tree and boostrapping {boot} times\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd,'/data',{inputpath:"/data",distancepath:"/output"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {distancepath}/hamming_distance_matrix.tsv {out}")
  sub.Popen(cmd).wait()
  if boot != 0:
      cmd = shlex.split(f"cp {distancepath}/bootstrapped_nj_trees.newick {out}")
      sub.Popen(cmd).wait()
      matrixpath = os.path.join(f"{distancepath}","matrixPermutations")
      treepath = os.path.join(f"{distancepath}","treePermutations")
      os.mkdir(matrixpath)
      os.mkdir(treepath)
      for i in range(1,(boot + 1)):
          cmd = shlex.split(f"mv {distancepath}/matrix_permutation_{i}.tsv {matrixpath}")
          sub.Popen(cmd).wait()
          cmd = shlex.split(f"mv {distancepath}/tree_permutation_{i}.newick {treepath}")
          sub.Popen(cmd).wait()

def consensusTree(out):
  logfile = os.path.join(out,'consensus.log')
  inputpath = os.path.join(out,"hammingDistance")
  consensuspath = os.path.join(out,"consensusTree")
  checkexists(consensuspath)

  # setup command
  cmd = f'bash -c \"sumtrees.py -s consensus -o /output/mrc95.nexus -f0.95 --percentages --decimals=0 /data/bootstrapped_nj_trees.newick\"'

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating 95% majority rule consensus tree\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd,'/data',{inputpath:"/data",consensuspath:"/output"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {consensuspath}/mrc95.nexus {out}")
  sub.Popen(cmd).wait()

def boostrapSupport(out):
  logfile = os.path.join(out,'support.log')
  supportpath = os.path.join(out,"bootstrapSupport")
  checkexists(supportpath)

  # setup commands
  cmd1 = f'bash -c \"sumtrees.py --decimals=0 -p -o /output/mrc95_boostrapSupport.nexus -t /data/mrc95.nexus /data/bootstrapped_nj_trees.newick\"'
  cmd2 = f'bash -c \"nexusToNewick.py /data/mrc95_boostrapSupport.nexus /data/\"'
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating support for nodes in the consensus tree\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd1,'/data',{out:"/data",supportpath:"/output"})
      outlog.write('***********\n')
      outlog.write('Converting nexus to newick\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd2,'/data',{supportpath:"/data"})
      outlog.write('***********\n')
  cmd = shlex.split(f"cp {supportpath}/mrc95_boostrapSupport.newick {out}")
  sub.Popen(cmd).wait()

# ------------------------------------------------------

def calculateHammingDistanceTree(tsvfile, out, transpose, boot):
    hammingDistanceTree(tsvfile, out, transpose, boot)
    if boot != 0:
        consensusTree(out)
        boostrapSupport(out)
