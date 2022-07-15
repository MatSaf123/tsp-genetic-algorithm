### Resolving travelling salesman problem with simple genetic algorithm

Made as a part of ML / AI use cases classes at University of Economics in Katowice, 2022.

Run with
`python3 cli.py <filepath> <selective pressure> <population size> <crossing rate> <mutation rate> <epochs>`
where filepath is the location of the file with data for the distances matrix (see examples in /data), and the rest or args are hyperparams for the algorithm.

An example:
`python3 cli.py data/berlin52.txt 5 200 0.75 0.05 1000`
