## MjolnirTree

MjolnirTree constructs a neigbor-joining tree using Hamming distance calculated from a binary gene presence/absence matrix. MjolnirTree uses a Docker container to maintain stability, reproducibility, portability and ease of use by keeping its dependencies in controlled environments.

### Using MjolnirTree

The input to MjolnirTree is a binary gene presence/absence matrix e.g. the output of pan-genome pipelines like [Roary](https://sanger-pathogens.github.io/Roary/). This matrix should be a tab-delimited file, with isolates as rows and genes as columns (isolates x genes). MjolnirTree has the option (-t) to transpose a matrix in the reverse orientation (genes x isolates). Boostrapping of the resulting neighbor-joining tree can be performed using the boot option, which outputs a 95% majority-rule consensus tree with node support reported as percentages rounded to integers.

```
usage: MjolnirTree [-h] tsv [options]

construct a neigbor-joining tree using a binary gene presence/absence matrix

required arguments:
  tsv   binary gene presence/absence matrix [isolates x genes], tab-delimited

optional arguments:
  -h, --help  show this help message and exit
  -o,   output directory, defaults to working directory
  -t,   transpose tsv
  boot, bootstrap tsv n times, defaults to 0
```
### Depenencies
MjolnirTree's dependencies are packaged in a [Docker container](https://github.com/AbigailShockey/MjolnirTree/blob/master/docker/Dockerfile). Matrix manipulation and boostrapping is performed using [pandas](https://pandas.pydata.org/) and [NumPy](https://numpy.org/). Hamming distance is calculated using [SciPy](https://www.scipy.org/). Trees are constructed and boostrap support is calculated using [DendroPy](https://dendropy.org/).

### Why name it MjolnirTree?

Hamming in Hamming distance sounds close to hammer. In Norse mythology, Mjolnir is the hammer of Thor, the Norse god of thunder. Hamming distances are used to produce the neighbor-joining tree, hence MjolnirTree.

### License

[GPLv3](https://github.com/AbigailShockey/MjolnirTree/blob/master/LICENSE)

### Author

Abigail C. Shockey
