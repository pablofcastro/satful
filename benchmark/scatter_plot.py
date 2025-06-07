"""
A simple script to produce the scatter plots of the benchmark 
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_10vars_satful = pd.read_csv("GurobiResults/results-10vars.csv")
df_20vars_satful = pd.read_csv("GurobiResults/results-20vars.csv")
df_30vars_satful = pd.read_csv("GurobiResults/results-30vars.csv")
df_40vars_satful = pd.read_csv("GurobiResults/results-40vars.csv")

i = 10
for df in (df_10vars_satful, df_20vars_satful, df_30vars_satful, df_40vars_satful) :
    df['file'] = f"{i}"+df['file']
    i = i + 10

df_satful = pd.concat([df_10vars_satful, df_20vars_satful, df_30vars_satful, df_40vars_satful])

df_10vars_fuzzysat = pd.read_csv("FuzzySAT/results-10vars.csv")
df_20vars_fuzzysat = pd.read_csv("FuzzySAT/results-20vars.csv")
df_30vars_fuzzysat = pd.read_csv("FuzzySAT/results-30vars.csv")
df_40vars_fuzzysat = pd.read_csv("FuzzySAT/results-40vars.csv")
i = 10
for df in (df_10vars_fuzzysat, df_20vars_fuzzysat, df_30vars_fuzzysat, df_40vars_fuzzysat) :
    df['file'] = f"{i}"+df['file']
    i = i + 10

for df in (df_10vars_fuzzysat, df_20vars_fuzzysat, df_30vars_fuzzysat, df_30vars_fuzzysat) :
    df.loc[df['result']=="TO",["time"]] = df["time"] * 1000
    df["time"] = df["time"] / 1000


df_10vars_scip = pd.read_csv("ScipResults/results-10vars.csv")
df_20vars_scip = pd.read_csv("ScipResults/results-20vars.csv")
df_30vars_scip = pd.read_csv("ScipResults/results-30vars.csv")
df_40vars_scip = pd.read_csv("ScipResults/results-40vars.csv")

i = 10
for df in (df_10vars_scip, df_20vars_scip, df_30vars_scip, df_40vars_scip) :
    df['file'] = f"{i}"+df['file']
    i = i + 10

df_fuzzysat = pd.concat([df_10vars_fuzzysat, df_20vars_fuzzysat, df_30vars_fuzzysat, df_40vars_fuzzysat])

df_scip = pd.concat([df_10vars_scip, df_20vars_scip, df_30vars_scip, df_40vars_scip])

count1 = df_satful["result"].value_counts().get('TO', 0)
count2 = df_fuzzysat["result"].value_counts().get('TO', 0)

merged = pd.merge(df_fuzzysat, df_satful, on='file', how='inner')
merged2 = pd.merge(df_fuzzysat, df_scip, on='file', how='inner')

# percent better without TO
count3 = len(merged[(merged["time_x"] > merged["time_y"]) & (merged["result_x"]!="TO")])/len(merged[merged["result_x"]!="TO"])

# percent better only UNSAT
count4 = len(merged[(merged["time_x"] > merged["time_y"]) & (merged["result_y"]=="UNSAT")])/len(merged[merged["result_y"]=="UNSAT"])

count5 = len(merged[(merged["time_x"] > merged["time_y"])])/len(merged)

#print(f"SATFuL: {count1}")
#print(f"SATFuzzy: {count2}")
#print(f"SATFuL better than SATFuzzy without UNSAT: {count3}")
#print(f"SATFuL better than SATFuzzy with UNSAT: {count5}")
#print(f"SATFuL better than SATFuzzy in UNSAT: {count4}")

# We create the plot
colors = np.where(merged['result_y'] == "UNSAT", 'red', 'blue')

sat_rows = merged[merged['result_y'] == "SAT"]
unsat_rows = merged[merged['result_y'] == "UNSAT"]
plt.scatter(sat_rows["time_x"], sat_rows["time_y"], color='b', label="SAT")
plt.scatter(unsat_rows["time_x"], unsat_rows["time_y"], color='r', label="UNSAT")


#merged.plot.scatter(x='time_x', y='time_y',c=colors)
plt.xlabel("SatFuzzy")
plt.ylabel("SATFuL(Gurobi)")

plt.xscale('log')
plt.yscale('log')
plt.plot([0.01, 300], [0.01, 300], 'k-', color = 'g')
plt.xlim(0.01, 300) 
plt.ylim(0.01, 300)
plt.legend() 
#plt.show()

plt.savefig("gurobi-plot.pdf",format="pdf")

merged2.plot.scatter(x='time_x', y='time_y',c=colors)
plt.xlabel("SatFuzzy")
plt.ylabel("SATFuL-Scip")

plt.xscale('log')
plt.yscale('log')
plt.plot([0.01, 300], [0.01, 300], 'k-', color = 'g')
plt.xlim(0.01, 300) 
plt.ylim(0.01, 300) 
#plt.show()
plt.savefig("scip-plot.pdf",format="pdf")

