import pandas as pd
import plotly.express as px
import streamlit as st
import math
import numpy as np
import ast



df = pd.read_csv("more_games2.csv")
df["Tag"] = df["Tag"].apply(lambda tags: ast.literal_eval(tags.replace('"', '')))
df["Developers"] = df["Developers"].apply(lambda developers: ast.literal_eval(developers.replace('"', '')))
df["Publishers"] = df["Publishers"].apply(lambda publishers: ast.literal_eval(publishers.replace('"', '')))

available_tags = []
available_developers = []
available_publishers = []

for index, value in df["Tag"].items(): available_tags.extend(value)
for index, value in df["Developers"].items(): available_developers.extend(value)
for index, value in df["Publishers"].items(): available_publishers.extend(value)
available_tags = list(set(available_tags))
available_developers = list(set(available_developers))
available_publishers = list(set(available_publishers))

st.set_page_config(
    page_title="Steam Games Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)

# Sidebar
st.sidebar.header("Filters:")

tags = st.sidebar.multiselect(
    "Select Tags:",
    options=pd.array(available_tags)
)

developers = st.sidebar.multiselect(
    "Select Developers:",
    options=pd.array(available_developers)
)

df_selection = df[df['Tag'].apply(lambda _tags: any(tag in _tags for tag in tags))] if len(tags) != 0 else df
df_selection = df_selection[df_selection['Developers'].apply(lambda _devs: any(dev in _devs for dev in developers))] if len(developers) != 0 else df_selection
# Always df_selection

# Main Page
st.title(":bar_chart: Games Statistics Dashboard")

# Top KPI 's
average_price = df_selection["Price"].agg("mean")
average_ccu = df_selection["CCU"].agg("mean")
total_positive_reviews = int(df_selection["Positive Reviews"].sum() if not math.isnan(df_selection["Positive Reviews"].sum()) else 0)
total_negative_reviews = int(df_selection["Negative Reviews"].sum() if not math.isnan(df_selection["Negative Reviews"].sum()) else 0)

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

grouped = df_selection.groupby(group_func)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.markdown("##### Average Price of Games:")
    st.markdown(f"US `${(average_price if not math.isnan(average_price) else 0):.2f}`")
with middle_column:
    st.markdown("##### Average Cost per Concurrent User (CCU):")
    st.markdown(f"US `${(average_ccu if not math.isnan(average_price) else 0):.2f}`")
with right_column:
    st.markdown("##### Dominant Tag (Category):")
    st.markdown(f"`{grouped[['Median Owners']].sum().idxmax()['Median Owners']}`")
st.markdown("---")
# Graph - Distribution for Median Playtime
median_playtime_grouped = grouped.sum()[["Median Playtime"]].sort_values(by="Median Playtime")
median_playtime_fig = px.bar(
    median_playtime_grouped,
    x="Median Playtime",
    y=median_playtime_grouped.index,
    orientation="h",
    labels={
        "index": "Tag (Category)"
    },
    title="<b>Distribution of Median Playtime</b>",
    color_discrete_sequence=["#0083B8"] * len(median_playtime_grouped),
    template="plotly_white"
)

# Create a DataFrame for the counts
counts_df = pd.DataFrame({'Sentiment': ['Positive', 'Negative'],
                          'Count': [total_positive_reviews, total_negative_reviews]})

# Create a pie chart using Plotly Express
reviews_fig = px.pie(counts_df, values='Count', names='Sentiment', title='Total Reviews')

left, right = st.columns(2)
left.plotly_chart(median_playtime_fig)
right.plotly_chart(reviews_fig)

left2, right2 = st.columns(2)

median_owned_grouped = grouped.sum()[["Median Owners"]].sort_values(by="Median Owners")
median_owned_fig = px.bar(
    median_owned_grouped,
    x="Median Owners",
    y=median_owned_grouped.index,
    orientation="h",
    labels={
        "index": "Tag (Category)"
    },
    title="<b>Distribution of Median Owners</b>",
    color_discrete_sequence=["#0083B8"] * len(median_owned_grouped),
    template="plotly_white"
)

left2.plotly_chart(median_owned_fig)





