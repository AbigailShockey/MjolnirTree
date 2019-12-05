#!/usr/bin/python3

import os,sys
import app.callDocker as cd
import shutil

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

  print("Calculating Hamming distances and constructing neighbor-joining tree")
  print(f"Bootstrapping {boot} times")

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write(f'Calculating hamming distance tree and boostrapping {boot} times\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd,'/data',{inputpath:"/data",distancepath:"/output"})
      outlog.write('***********\n')
  shutil.copyfile(os.path.join(distancepath,'hamming_distance_matrix.tsv'),os.path.join(out,'hamming_distance_matrix.tsv'))
  if boot != 0:
      shutil.copyfile(os.path.join(distancepath,'bootstrapped_nj_trees.newick'),os.path.join(out,'bootstrapped_nj_trees.newick'))
      matrixpath = os.path.join(f"{distancepath}","matrixPermutations")
      treepath = os.path.join(f"{distancepath}","treePermutations")
      os.mkdir(matrixpath)
      os.mkdir(treepath)
      for i in range(1,(boot + 1)):
          shutil.move(os.path.join(distancepath,f'matrix_permutation_{i}.tsv'),os.path.join(matrixpath,f'matrix_permutation_{i}.tsv'))
          shutil.move(os.path.join(distancepath,f'tree_permutation_{i}.newick'),os.path.join(treepath,f'tree_permutation_{i}.newick'))

def consensusTree(out):
  logfile = os.path.join(out,'consensus.log')
  inputpath = os.path.join(out,"hammingDistance")
  consensuspath = os.path.join(out,"consensusTree")
  checkexists(consensuspath)

  # setup command
  cmd = f'bash -c \"sumtrees.py -s consensus -o /output/mrc95.nexus -f0.95 --percentages --decimals=0 /data/bootstrapped_nj_trees.newick\"'

  print("Calculating 95% majority rule consensus tree")

  # denote logs
  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating 95% majority rule consensus tree\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd,'/data',{inputpath:"/data",consensuspath:"/output"})
      outlog.write('***********\n')
  shutil.copyfile(os.path.join(consensuspath,'mrc95.nexus'),os.path.join(out,'mrc95.nexus'))

def boostrapSupport(out):
  logfile = os.path.join(out,'support.log')
  supportpath = os.path.join(out,"bootstrapSupport")
  checkexists(supportpath)

  # setup commands
  cmd1 = f'bash -c \"sumtrees.py --decimals=0 -p -o /output/mrc95_boostrapSupport.nexus -t /data/mrc95.nexus /data/bootstrapped_nj_trees.newick\"'

  print("Calculating support for nodes in the consensus tree")

  cmd2 = f'bash -c \"nexusToNewick.py /data/mrc95_boostrapSupport.nexus /data/\"'

  print("Converting nexus to newick")

  with open(logfile,'a') as outlog:
      outlog.write('***********\n')
      outlog.write('Calculating support for nodes in the consensus tree\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd1,'/data',{out:"/data",supportpath:"/output"})
      outlog.write('***********\n')
      outlog.write('Converting nexus to newick\n')
      results = cd.call('ashockey/mjolnir-tree:latest',cmd2,'/data',{supportpath:"/data"})
      outlog.write('***********\n')
  shutil.copyfile(os.path.join(supportpath,'mrc95_boostrapSupport.newick'),os.path.join(out,'mrc95_boostrapSupport.newick'))

# ------------------------------------------------------

def calculateHammingDistanceTree(tsvfile, out, transpose, boot):
    hammingDistanceTree(tsvfile, out, transpose, boot)
    if boot != 0:
        consensusTree(out)
        boostrapSupport(out)
