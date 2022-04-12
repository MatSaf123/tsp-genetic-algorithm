import sys
from main import run_simple_genetic_algorithm

print("Number of arguments:", len(sys.argv), "arguments.")
print("Argument List:", str(sys.argv))

params = sys.argv[1:]
if len(params) != 6:
    raise Exception(
        f"provided incorrect number of args (6 needed, got: {len(params)})"
    )

path = params[0]
k = int(params[1])
n = int(params[2])
cc = float(params[3])
cm = float(params[4])
epochs = int(params[5])

run_simple_genetic_algorithm(path, k, n, cc, cm, epochs)
