#!/usr/bin/python3

import os,sys
import argparse
import dendropy

# This script converts a phylogenetic tree in nexus format to newick format

# setup argparser to display help if no arguments
class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# determine command line arguments and get path
parser = ArgParser(description='Convert a phylogenetic tree in nexus format to newick format')
parser.add_argument('nexus', type=str, help="Phylogenetic tree in nexus format")
parser.add_argument('out', type=str, help="Output directory")

args = parser.parse_args()

treeFile = os.path.abspath(args.nex)
out = args.out

newickHandle = os.path.basename(treeFile).split(".")[0] + ".newick"
newickTree = os.path.join(out,newickHandle)
nexusTree = dendropy.Tree.get(path=treeFile, schema="nexus")
nexusTree.write(path=newickTree, schema="newick")
