# NOTE: This is a random test file, which is not necessary
# You can delete it if you want
import pandas as pd
import ast

df = pd.read_csv("games.csv")

df["Tag"] = df["Tag"].apply(lambda tags: ast.literal_eval(tags))

available_tags = []
available_developers = []
available_publishers = []
# list_of_developers = []
# list_of_publishers = []

for index, value in df["Tag"].items(): available_tags.extend(value)
for index, value in df["Developers"].items(): available_tags.extend(value)
for index, value in df["Publishers"].items(): available_tags.extend(value)
available_tags = [t for t in list(set(available_tags)) if len(t) > 1]
available_developers = [t for t in list(set(available_developers)) if len(t) > 1]
available_publishers = [t for t in list(set(available_publishers)) if len(t) > 1]


indices = {}
def group_func(x):
    global indices
    if x in indices.keys():
        indices[x] += 1
    else: indices[x] = 0
    data = df["Tag"].iloc[x]
    if len(data) > indices[x]:
        return data[indices[x]]
    return None
# Use an index dictionary to test
print(df)
df_selection = df[df['Tag'].apply(lambda _tags: any(tag in _tags for tag in available_tags))]
#grouped = df_selection.groupby(group_func)
grouped = df.groupby(group_func)
print(grouped["Median Playtime"].apply(lambda group: group.nlargest(1).index.tolist()[0]).nlargest(3).index.tolist())
#print(available_tags)