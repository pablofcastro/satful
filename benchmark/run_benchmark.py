"""
This is a basic script for running the benchmark with fuzzysat, it saves the results as a
.csv files
"""
import sys, os, subprocess, csv, re, signal

command = '-g'
logic = 'luk'
if sys.argv[1] == "-h" : 
    print(f"""Usage: python run_benchmark.py [-g | -s] [-product | -luk]:
              -h : prints this help
              -g : run the benchmarks with gurobi
              -s : run the benchmarks with scip
              -luk: run the benchmarks for Lukasiewicz logic
              -product: run the benchmarks for Product logic
             Example: python run_benchmarks -g -product (runs the product logic benchmarks with Gurobi)
          """)
    exit()
if sys.argv[1] == "-scip" :
    command = '-s'
    print("Using SCIP solver")
else :
    print("Using Gurobi solver")

if sys.argv[2] == "-product" :
    logic = 'prod'
main_dir = "../"
if logic == '-luk' : 
    datasets_dir = "randomClauses"
else :
    datasets_dir = "productRandomClauses"
benchmarks = ["10vars","20vars","30vars","40vars"]
#benchmarks = ["10vars","20vars","30vars"]
for b in benchmarks :
    results = [] # the results are a list of dictionaries
    for file in os.listdir(datasets_dir+"/"+b+"/") :
        print("running file: "+file)
        row = {}
        row["file"] = file
        try :
            result = subprocess.run(['python', 'pfl_sat.py',command,'-i',f"""../benchmark/{datasets_dir}/"""+b+"/"+file], timeout=300, cwd="../PL/",capture_output=True).stdout.decode()
            print(result)
            for line in result.splitlines() :
                words = line.split()
                if line.startswith("Time") : 
                    row["time"] = words[2]
                elif line.startswith("Result") :
                    row["result"] = words[2]
                elif line.startswith("time out") :
                    row["time"] = "TO"
        except :
            row["result"] = "TO"
            row["time"]   = "300"
        # we add the result
        results.append(row)
    # we write the results to a .csv file
    keys = results[0].keys()
    folder = "GurobiResults/"
    if command == '-s' :
        folder = "ScipResults/"
    name = "results-"+logic
    with open(folder+f'{name}-{b}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)
