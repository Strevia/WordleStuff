from datetime import datetime
import pandas as pd
data = []
with open("statesearch.txt", "r") as f:
    for line in f:
        data.append(line.strip())
output = "Updated at: " + str(datetime.now()) + "\nwords,count,score,index\n"
written = []
for c, d in enumerate(data):
    d = d.replace("->", "")
    d = d.replace("[", "")
    d = d.replace("]", "")
    d = d.replace("(", "")
    d = d.replace(")", "")
    d = d.replace("  ", " ")
    d = d.replace(",", "")
    d = d.replace("'", "")
    line = d.split(" ")
    words = sorted(line[:-1])
    if sorted(words) in written:
        continue
    written.append(sorted(words))
    score = line[-1]
    output += '|'.join(words) + "," + score + "," + str(len(words)) + "," + str(c+1) + "\n"
with open("statesearch.csv", "w") as f:
    f.write(output)
df = pd.read_csv("statesearch.csv", skiprows=1)
df.sort_values(by=['count', 'score', 'index'], ascending=[True, True, True], inplace=True)
with open("statesearch.csv", "w") as f:
    f.write("Updated at: " + str(datetime.now()) + "\n")
df.to_csv("statesearch.csv", mode = "a", index=False)
