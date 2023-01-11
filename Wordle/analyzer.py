from datetime import datetime
import pandas as pd
from tqdm import tqdm
data = []
with open("statesearch.txt", "r") as f:
    for line in f:
        data.append(line.strip())
output = "Updated at: " + str(datetime.now()) + "\nwords,count,score,index\n"
written = []
for c, d in tqdm(enumerate(data), total = len(data), leave = False):
    split = d.split(",")
    guesses = split[0].split(" ") + [split[1]]
    if sorted(guesses) in written:
        continue
    guesses.sort()
    written.append(sorted(guesses))
    output += f"{' '.join(guesses)}, {len(split[0].split(' ')) + 1}, {split[2]}, {c}\n"
with open("statesearch.csv", "w") as f:
    f.write(output)
df = pd.read_csv("statesearch.csv", skiprows=1)
df.sort_values(by=['count', 'score', 'index'], ascending=[False, True, True], inplace=True)
with open("statesearch.csv", "w") as f:
    f.write("Updated at: " + str(datetime.now()) + "\n")
df.to_csv("statesearch.csv", mode = "a", index=False)
