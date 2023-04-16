# TSP with Genetic Algorithm

Resolving Travelling Salesman Problem with simple genetic algorithm implementation made in python. Made as a part of ML / AI use cases classes at University of Economics in Katowice, 2022.

# Run

I don't recall installing any dependencies other than some linting/formatting tools, so it's possible it will work straight out of box. But if not, then do the usual python venv setup steps:

1. Create python venv via your favorite tool (e.g. `python3 -m venv venv`) and activate it.
2. Run
```
pip install -r requirements.txt
```
3. Run with `python3 cli.py <filepath> <selective pressure> <population size> <crossing rate> <mutation rate> <epochs>`
where filepath is the location of the file with data for the distances matrix (see examples in /data), and the rest or args are hyperparams for the algorithm.

An example:
`python3 cli.py data/berlin52.txt 5 200 0.75 0.05 1000`
