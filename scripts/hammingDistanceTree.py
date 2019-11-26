#!/usr/bin/env python 3

import os,sys
import argparse
import pandas as pd
import scipy
from scipy import spatial
from scipy.spatial.distance import pdist,squareform
import numpy as np
import random
import dendropy

# This script takes a binary gene presence/absence file, calcualtes a pairwise hamming distance matrix and
# returns a neihbor-joining tree in newick format. It can also perform boostrapping

# setup argparser to display help if no arguments
class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# determine command line arguments and get path
parser = ArgParser(description='Calculate pairwise hamming distance matrix from gene prensece/absence matrix and create nj tree')
parser.add_argument('tsv', type=str, help="Binary gene presence and absence file (tab delimited)")
parser.add_argument('out', type=str, help="Output directory")
parser.add_argument('boot', type=int, help="Perform boostrapping n times")
parser.add_argument('transpose', type=str, help="Transpose tsv")

args = parser.parse_args()

def transpose_mat(dat):
    tdf = dat.transpose()
    return tdf

def calc_hamming_distance(dat, outMatrix):
    hdm = pd.DataFrame(
        squareform(pdist(dat, metric = 'hamming')),
        columns = dat.index,
        index = dat.index)
    hdm.to_csv(outMatrix, sep='\t', encoding='utf-8')

def calc_nj_tree(outMatrix, outTree):
    with open(outMatrix) as dm:
        pdm = dendropy.PhylogeneticDistanceMatrix.from_csv(
                dm,
                is_first_row_column_names=True,
                is_first_column_row_names=True,
                is_allow_new_taxa=True,
                delimiter="\t")
    nj_tree = pdm.nj_tree()
    nj_tree.write(
        path=outTree,
        schema="newick")
    return nj_tree

# Set pandas display options (for printing)
pd.options.display.max_rows = 10
pd.options.display.max_columns = 5

tsvfile = os.path.abspath(args.tsv)
prefix = args.prefix
out = args.out

# read gene presence/absence tsv, treating first column as rownames and first row as column names
df = pd.read_csv(tsvfile, sep="\t", index_col=0, header=0)

# transpose gene presence/absence tsv and write to file
if args.transpose == "True":
    df = transpose_mat(df)

# hdm name and path
matrixOut = os.path.join(out,f"hamming_distance_matrix.tsv")

# calculate hdm
calc_hamming_distance(df, matrixOut)

# nj tree name and path
treeOut = os.path.join(out,f"nj_tree.newick")

# calculate nj tree from hdm
calc_nj_tree(matrixOut, treeOut)

if args.boot != 0:
    # create empty list of trees
    trees = dendropy.TreeList()

    # begin bootstrapping
    for i in range(1,(args.b + 1)):
        # randomly sample tsv columns with replacement
        rcols = np.random.choice(list(df.columns.values),len(list(df.columns.values)), replace=True)
        rdf = df[rcols]
        
        # randomly re-order tsv rows (see "jumble" option in boot.phylo function from R package ape)
        rdf = rdf.sample(frac=1, replace=False)
        
        # permuted hdm name and path
        rMatrixOut = os.path.join(out,f"matrix_permutation_{i}.tsv")
        
        # calculate hdm of permuted tsv
        calc_hamming_distance(rdf, rMatrixOut)
        
        # permuted nj tree name and path
        rTreeOut = os.path.join(out,f"tree_permutation_{i}.newick")
        
        # calculate nj tree from hdm of permuted tsv
        rnj_tree = calc_nj_tree(rMatrixOut, rTreeOut)
        
        # append permuted nj tree
        trees.append(rnj_tree)

    # write all permuted nj trees to file
    trees.write(
        path=os.path.join(out,"bootstrapped_nj_trees.newick"),
        schema="newick")
