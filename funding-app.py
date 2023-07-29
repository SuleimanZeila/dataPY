import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title='Global - Crisis Figures Data', page_icon='star', layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("Global - Crisis Figures Data")

df = pd.read_csv("Data_ ReliefWeb Crisis Figures Data - latest_figures.csv")


countries_list = df["crisis_name"].unique()
org_list = df["figure_source"].unique()

with st.sidebar:
	st.sidebar.header('Filter')
	# Using object notation
	add_countries = st.sidebar.selectbox(
	    "Choose a countries",
	    (countries_list)
	)
	filtered_df = df[df["crisis_name"] == add_countries]
	org_list = filtered_df["figure_source"].unique()
	add_org = st.sidebar.selectbox(
	    "Choose a Organization",
	    (org_list)
	)
	df = filtered_df[filtered_df["figure_source"] == add_org]
	rows = len(df.axes[0])

country_counts = df["crisis_name"].value_counts()

total_countries = len(country_counts)

org_counts = df["figure_source"].value_counts()
sum_count = df["figure_value"].sum()

# Get the total number of unique countries
total_org = len(org_counts)

df["figure_date"] = pd.to_datetime(df["figure_date"])

# Get the first date (minimum date) and the last date (maximum date) in the "figure_date" column
first_date = df["figure_date"].min()
last_date = df["figure_date"].max()


st.write(f'## Data {add_countries}')

col1, col2 = st.columns(2)
st.write('---')
col5, col6= st.columns(2)
st.write('---')
col1.write(f"#### Number of Projected completed by {add_org}")
col1.write(f"#### *{rows}*")

# col3.write("#### Number of Org's")
# col3.write(f"#### *{total_org}*")

formatted_number = "{:,}".format(sum_count)
col2.write("#### Sum Spent")
col2.write(f"#### *$ {formatted_number}*")

# st.dataframe(df)


df["figure_date"] = pd.to_datetime(df["figure_date"])

# Extract only the date part (without time)
df["figure_date"] = df["figure_date"].dt.date

# Get the first date (minimum date) and the last date (maximum date) in the "figure_date" column
first_date = df["figure_date"].min()
last_date = df["figure_date"].max()

print("First Date:", first_date)
print("Last Date:", last_date)

col5.write("#### Start Date")
col5.write(f"#### {first_date}")

col6.write("#### Last Date")
col6.write(f"#### {last_date}")

# df = df.sort_values(by="figure_date")

# Sort the DataFrame by "figure_date" (optional, but good practice)
df = df.sort_values(by="figure_date")

# Create the line plot
plt.figure(figsize=(10, 6))  # Set the size of the plot (width, height)
plt.plot(df["figure_date"], df["figure_value"], marker='o', linestyle='-', color='b', label="Figure Value")

# Set labels and title
plt.xlabel("Date", fontsize=12)
plt.ylabel("Figure Value", fontsize=12)
plt.title(f"Line Plot of Figure Value over Time for {add_org} in {add_countries}", fontsize=14)
plt.grid(True)  # Show grid lines
plt.legend()    # Show legend

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Beautify the plot with a light background, grid lines, and more
plt.style.use('seaborn-whitegrid')
plt.tight_layout()

# Show the plot
st.pyplot()

# Optionally, display the DataFrame in Streamlit
# st.dataframe(df)


newdf = filtered_df[filtered_df["crisis_name"] == add_countries]
newdf = newdf.groupby('figure_source')['figure_value'].sum().reset_index()
# st.dataframe(newdf)



# fig, ax = plt.subplots()
# ax.pie(newdf["figure_value"], labels=newdf["figure_source"], autopct='%1.1f%%', startangle=90)
# ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Set title
# ax.set_title(f"Contributions by All Organizations in {add_countries}")
# st.write('---')

# Show the pie chart in Streamlit
# st.pyplot(fig)

# newdf = pd.DataFrame(data)

# Create the pie chart
fig, ax = plt.subplots(figsize=(6, 6))  # Set the size of the chart

# Set colors for the pie chart
colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']

# Draw the pie chart
wedges, texts, autotexts = ax.pie(newdf["figure_value"],
                                  labels=newdf["figure_source"],
                                  autopct=lambda pct: f"{pct:.1f}% ({int(pct * sum(newdf['figure_value']) / 100)})",
                                  startangle=90,
                                  colors=colors)

# Set font size and properties for text labels
for text in texts:
    text.set_fontsize(8)
    text.set_fontweight('bold')

# Set font size and properties for percentage labels
for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_fontweight('bold')

# Set title for the pie chart
ax.set_title(f"Contributions by Organizations in {add_countries}", fontsize=14)

# Draw a circle at the center of the pie chart to make it look like a donut chart
centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig.gca().add_artist(centre_circle)

# Equal aspect ratio ensures that pie is drawn as a circle
ax.axis('equal')

# Hide the axes
ax.axis('off')

# Show the pie chart in Streamlit
st.pyplot(fig)
