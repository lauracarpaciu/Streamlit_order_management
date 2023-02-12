# import gender_guesser.detector as gender
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
# from streamlit_lottie import st_lottie
st.set_page_config(page_title="Analiza tendintelor de comsum App", layout="wide")

### Data Import ###
import pandas as pd
DATE_COLUMN = 'Order Date'
SHEET_ID = '1EKX-KgMQ0tCJrqLTlxmBSECpK8iYMWnyq9WwROXZ47Y'
SHEET_NAME = 'cleaned'
DATA_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]).dt.year

    return data
df_database=load_data(10000)

# streamlit_lottie(df_database, speed=1, height=200, key="initial")
# st.subheader('Raw data')
# st.write(df_database)
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Analysis of the consumption trends of a stationery store")


with row0_2:
    add_vertical_space()

row0_2.subheader(
    "A Streamlit web app by [Laura Carpaciu](https://lauracarpaciu.github.io), [Laura GitHub Repository](https://github.com/lauracarpaciu?tab=repositories))"
)
row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    st.markdown("")
    see_data = st.expander('You can click here to see the data set 👉')
    with see_data:
        st.dataframe(data=df_database.reset_index(drop=True))
st.text('')

u_orders = len(df_database["Row ID"].unique())
u_subcat = len(df_database["Sub-Category"].unique())

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
with row3_1:
    st.subheader("Placed orders")
    year_df = pd.DataFrame(df_database["Order Date"].dropna().value_counts()).reset_index()
    year_df = year_df.sort_values(by="index")
    year_df.columns = ["Year", "Count"]
    fig = px.bar(
        year_df,
        x="Year",
        y="Count",
        title="Orders by year",
        color_discrete_sequence=["#7b2e80"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "It can be seen that a number of **{} orders from {} subcategories,** with {} being the most popular category! This is the trend for this store.".format(
            u_orders, u_subcat, df_database["Category"].mode()[0]
        )
    )


with row3_2:
    st.subheader("The consumption trend")
    # plots a bar chart of the dataframe df by book.publication year by count in plotly. columns are publication year and count
    age_df = pd.DataFrame(df_database["Order Date"].value_counts()).reset_index()
    age_df = age_df.sort_values(by="index")
    age_df.columns = ["Order Date", "Count"]
    fig = px.bar(
        age_df,
        x="Order Date",
        y="Count",
        title="Orders by year",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    avg_office_year = str(int(np.mean(pd.to_numeric(df_database["Order Date"]))))
    row_young = df_database.sort_values(by="Order Date", ascending=False).head(1)
    youngest_office = row_young["Product Name"].iloc[0]
    row_old = df_database.sort_values(by="Order Date").head(1)
    oldest_office = row_old["Product Name"].iloc[0]

    st.markdown(
        "It can be seen that the average of the orders is in  **{}**, with the oldest product sold **{}** and the latest product sold  **{}**.".format(
            avg_office_year, oldest_office, youngest_office
        )
    )


add_vertical_space()
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row4_1:
    st.subheader("What is the most common subcategory?")
    author_categ_df = pd.DataFrame(
        df_database["Sub-Category"].value_counts(normalize=True)
    ).reset_index()
    # plot bar plot of gender by percentage in plotly
    author_categ_df.columns = ["Sub-Category", "Percentage"]
    fig = px.bar(
        author_categ_df,
        x="Sub-Category",
        y="Percentage",
        title="Percentage of orders according to subcategory",
        color_discrete_sequence=["#444657"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "The chart shows the consumption trend for each subcategory ")


with row4_2:
    st.subheader("What quantity is most frequently ordered?")
    fig = px.histogram(
        df_database,
        x="Quantity",
        title="The consumption trend ",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="The ordered quantity ")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "You can see the distribution of the quantity ordered by the store's customers!"
    )

add_vertical_space()
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row5_1:
    st.subheader("The distribution of the discount applied for the sale")
    fig = px.histogram(
        df_database,
        x="Discount",
        title="The discount ' distribution",
        color_discrete_sequence=["#4c3ca3"],
    )
    fig.update_xaxes(title_text="Discount")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    office_len_avg = round(np.mean(pd.to_numeric(df_database["Discount"].dropna())))
    office_len_max = pd.to_numeric(df_database["Discount"]).max()
    row_long = df_database[pd.to_numeric(df_database["Discount"]) == office_len_max]
    longest_office = row_long["Sub-Category"].iloc[0]

    st.markdown(
        "The average discount is **{}**, and the biggest discount is for the subcategory **{}**!".format(
            office_len_avg, longest_office, int(office_len_max)
        )
    )

with row5_2:

    st.subheader("The distribution of orders by region, on time")
    year_office_df = pd.DataFrame(
        df_database.groupby(["Order Date"])["Region"].value_counts(normalize=True)
    )
    year_office_df.columns = ["Percentage"]
    year_office_df.reset_index(inplace=True)
    year_office_df = year_office_df[year_office_df["Order Date"] != ""]
    year_office_df["Order Date"] = pd.to_timedelta(year_office_df["Order Date"])
    # plot line plot in plotly of year_author_df with x axis as read_at_year, y axis is percentage, color is author gender
    fig = px.line(
        year_office_df,
        x="Order Date",
        y="Percentage",
        color="Region",
        title="The percentage of orders depending on the region over time",
    )
    fig.update_xaxes(title_text="Year")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "You can see the percentage of orders depending on each region and how it has changed over time."
    )
add_vertical_space()
row7_spacer1, row7_1, row7_spacer2 = st.columns((0.1, 3.2, 0.1))

st.markdown("***")
st.markdown(
        "Thank you for reading this review! I appreciate the feedback, and if you want to know more you can find me at [website](https://lauracarpaciu.github.io) ")

