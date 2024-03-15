import pandas as pd
import ast

df = pd.read_csv("more_games2.csv")

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
df_selection = df[df['Tag'].apply(lambda _tags: any(tag in _tags for tag in ["Racing", "Indie", "Adventure"]))]
grouped = df_selection.groupby(group_func)
print(grouped[["Median Playtime"]].sum().idxmax()["Median Playtime"])
#print(available_tags)