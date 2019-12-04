## MjolnirTree

MjolnirTree constructs a neigbor-joining tree using hamming distances calculated from a binary gene presence/absence matrix. MjolnirTree uses a Docker container to maintain stability, reproducibility, portability and ease of use by keeping its dependencies in controlled environments.

#### MjolnirTree

The input to MjolnirTree is a binary gene presence/absence matrix. This matrix should be a tab-delimited file, with isolates as rows and genes as columns (isolates x genes). MjolnirTree has the option (-t) to transpose a matrix in the reverse orientation (genes x isolates). Boostrapping of the resulting neighbor-joining tree can be performed using the boot option.

```
usage: MjolnirTree [-h] tsv [options]

construct a neigbor-joining tree using hamming distances calculated from a \
  binary gene presence/absence matrix

required arguments:
  tsv   binary gene presence/absence matrix [isolates x genes], tab-delimited

optional arguments:
  -h, --help  show this help message and exit
  -o,   output directory, defaults to working directory
  -t,   transpose, transpose tsv
  boot, bootstrap, bootstrap tsv n times
```
