# import gender_guesser.detector as gender
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Hotel booking demands Analysis App", layout="wide")

### Data Import ###

DATE_COLUMN = 'arrival_date_year'
DATA_URL = ('C:/Users/Mirela/PycharmProjects/Hotel Booking/data_cleaned.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATE_COLUMN] = pd.to_timedelta(data[DATE_COLUMN])

    return data

df_database = load_data(119390)

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Analyzing Your Hotel demand Habits")

with row0_2:
    add_vertical_space()

row0_2.subheader(
    "A Streamlit web app by [Tyler Richards](http://www.tylerjrichards.com), get my new book on Streamlit [here!](https://www.amazon.com/Getting-Started-Streamlit-Data-Science/dp/180056550X)"
)
row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))
with row1_1:
    st.markdown(
        "Hey there! Welcome to Tyler's Goodreads Analysis App. This app scrapes (and never keeps or stores!) the books you've read and analyzes data about your book list, including estimating the gender breakdown of the authors, and looking at the distribution of the age and length of book you read. After some nice graphs, it tries to recommend a curated book list to you from a famous public reader, like Barack Obama or Bill Gates. One last tip, if you're on a mobile device, switch over to landscape for viewing ease. Give it a go!"
    )
    st.markdown(
        "**To begin, please enter the link to your [Goodreads profile](https://www.goodreads.com/) (or just use mine!).** 👇"
    )




line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
u_books = len(df_database["id"].unique())
u_authors = len(df_database["country"].unique())
with row3_1:
    st.subheader("Arrival")
    year_df = pd.DataFrame(df_database["arrival_date_year"].dropna().value_counts()).reset_index()
    year_df = year_df.sort_values(by="index")
    year_df.columns = ["Year", "Count"]
    fig = px.bar(
        year_df,
        x="Year",
        y="Count",
        title="Arrival by Year",
        color_discrete_sequence=["#7b2e80"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "It looks like you've read a grand total of **{} arrivals with {} countrys,** with {} being your most read author! That's awesome. Here's what your reading habits look like since you've started using Goodreads.".format(
            u_books, u_authors, df_database["hotel"].mode()[0]
        )
    )


with row3_2:
    st.subheader("Week nights")
    # plots a bar chart of the dataframe df by book.publication year by count in plotly. columns are publication year and count
    age_df = pd.DataFrame(df_database["stays_in_week_nights"].value_counts()).reset_index()
    age_df = age_df.sort_values(by="index")
    age_df.columns = ["stays in week nights", "count"]
    fig = px.bar(
        age_df,
        x="stays in week nights",
        y="count",
        title="Stays in week nights",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="stays in week nights")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    avg_book_year = str(int(np.mean(pd.to_numeric(df_database["stays_in_week_nights"]))))
    row_young = df_database.sort_values(by="stays_in_week_nights", ascending=False).head(1)
    youngest_book = row_young["lead_time"].iloc[0]
    row_old = df_database.sort_values(by="stays_in_week_nights").head(1)
    oldest_book = row_old["lead_time"].iloc[0]

    st.markdown(
        "Looks like the average stays is around **{}**, with your oldest lead time being **{}** and your youngest being **{}**.".format(
            avg_book_year, oldest_book, youngest_book
        )
    )
    # st.markdown(
    #     "Note that the publication date on Goodreads is the **last** publication date, so the data is altered for any book that has been republished by a publisher."
    # )

add_vertical_space()
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row4_1:
    author_gender_df = pd.DataFrame(
        df_database["meal"].value_counts(normalize=True)
    ).reset_index()
    # plot bar plot of gender by percentage in plotly
    author_gender_df.columns = ["meal", "Percentage"]
    fig = px.bar(
        author_gender_df,
        x="meal",
        y="Percentage",
        title="Percentage of Books by Gender",
        color_discrete_sequence=["#444657"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "To get the gender breakdown of the books you have read, this next bit takes the first name of the authors and uses that to predict their gender. These algorithms are far from perfect, and tend to miss non-Western/non-English genders often so take this graph with a grain of salt."
    )
    st.markdown(
        "Note: the package I'm using for this prediction outputs 'andy', which stands for androgenous, whenever multiple genders are nearly equally likely (at some threshold of confidence). It is not, sadly, a prediction of a new gender called andy."
    )

with row4_2:
    st.subheader("How do Goodreads Users Rate Your Reads?")
    fig = px.histogram(
        df_database,
        x="meal",
        title="Goodreads User Ratings",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="Average Rating")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Here is the distribution of average rating by other Goodreads users for the books that you've read. Note that this is a distribution of averages, which explains the lack of extreme values!"
    )

add_vertical_space()
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row5_1:
    st.subheader("Book Length Distribution")
    fig = px.histogram(
        df_database,
        x="lead_time",
        title="Book Length Distribution",
        color_discrete_sequence=["#4c3ca3"],
    )
    fig.update_xaxes(title_text="Number of Pages")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    book_len_avg = round(np.mean(pd.to_numeric(df_database["lead_time"].dropna())))
    book_len_max = pd.to_numeric(df_database["lead_time"]).max()
    row_long = df_database[pd.to_numeric(df_database["lead_time"]) == book_len_max]
    longest_book = row_long["hotel"].iloc[0]

    st.markdown(
        "Your average book length is **{} pages**, and your longest book read is **{} at {} pages!**.".format(
            book_len_avg, longest_book, int(book_len_max)
        )
    )



add_vertical_space()
row6_space1, row6_1, row6_space2, row6_2, row6_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
with row5_2:
    st.subheader("Gender Distribution Over Time")
    year_author_df = pd.DataFrame(
        df_database.groupby(["arrival_date_year"])["market_segment"].value_counts(normalize=True)
    )
    year_author_df.columns = ["Percentage"]
    year_author_df.reset_index(inplace=True)
    year_author_df = year_author_df[year_author_df["arrival_date_year"] != ""]
    year_author_df["arrival_date_year"] = pd.to_timedelta(year_author_df["arrival_date_year"])
    # plot line plot in plotly of year_author_df with x axis as read_at_year, y axis is percentage, color is author gender
    fig = px.line(
        year_author_df,
        x="arrival_date_year",
        y="Percentage",
        color="market_segment",
        title="Percent of Books by Gender Over Time",
    )
    fig.update_xaxes(title_text="Year Read")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Here you can see the gender distribution over time to see how your reading habits may have changed."
    )
    st.markdown(
        "Want to read more books written by women? [Here](https://www.penguin.co.uk/articles/2019/mar/best-books-by-female-authors.html) is a great list from Penguin that should be a good start (I'm trying to do better at this myself!)."
    )


