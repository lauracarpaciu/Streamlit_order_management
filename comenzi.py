# import gender_guesser.detector as gender
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from streamlit_extras.add_vertical_space import add_vertical_space
# from streamlit_lottie import st_lottie
st.set_page_config(page_title="Analiza tendintelor de comsum App", layout="wide")

### Data Import ###

DATE_COLUMN = 'Order Date'
DATA_URL = ('C:/Users/Mirela/PycharmProjects/hotel/cleaned.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]).dt.year

    return data
df_database=load_data(10000)
# streamlit_lottie(df_database, speed=1, height=200, key="initial")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
)

row0_1.title("Analiza tendintelor de consum ale unui magazin universal")


with row0_2:
    add_vertical_space()

row0_2.subheader(
    "A Streamlit web app by [Laura Carpaciu](https://lauracarpaciu.github.io), [Laura GitHub Repository](https://github.com/lauracarpaciu/Streamlit_order_management))"
)
row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
with row2_1:
    default_username = st.selectbox(
        "Selecteaza numele autorului",
        (
            "laura carpaciu",
                  ),
    )

u_books = len(df_database["Row ID"].unique())
u_authors = len(df_database["Sub-Category"].unique())

st.write("")
row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)
with row3_1:
    st.subheader("Comenzi")
    year_df = pd.DataFrame(df_database["Order Date"].dropna().value_counts()).reset_index()
    year_df = year_df.sort_values(by="index")
    year_df.columns = ["Year", "Count"]
    fig = px.bar(
        year_df,
        x="Year",
        y="Count",
        title="Comenzi anuale",
        color_discrete_sequence=["#7b2e80"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Se poate observa ca s-au plasat un numar de **{} comenzi din {} sub categorii,** cu {} fiind cea mai apreciata subcategorie! Este foarte interesant rezultatul. Acesta este tendinta pentru acest magazin.".format(
            u_books, u_authors, df_database["Category"].mode()[0]
        )
    )


with row3_2:
    st.subheader("Tendinte")
    # plots a bar chart of the dataframe df by book.publication year by count in plotly. columns are publication year and count
    age_df = pd.DataFrame(df_database["Order Date"].value_counts()).reset_index()
    age_df = age_df.sort_values(by="index")
    age_df.columns = ["Order Date", "count"]
    fig = px.bar(
        age_df,
        x="Order Date",
        y="count",
        title="Order Date",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="Data comenzii")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    avg_book_year = str(int(np.mean(pd.to_numeric(df_database["Order Date"]))))
    row_young = df_database.sort_values(by="Order Date", ascending=False).head(1)
    youngest_book = row_young["Product Name"].iloc[0]
    row_old = df_database.sort_values(by="Order Date").head(1)
    oldest_book = row_old["Product Name"].iloc[0]

    st.markdown(
        "Se observa ca media comenzilor este in  **{}**, cu cel mai vechi produs vandut **{}** si cel mai recent produs vandut  **{}**.".format(
            avg_book_year, oldest_book, youngest_book
        )
    )


add_vertical_space()
row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)


with row4_1:
    st.subheader("Care este subcategoria cel mai des intalnita?")
    author_gender_df = pd.DataFrame(
        df_database["Sub-Category"].value_counts(normalize=True)
    ).reset_index()
    # plot bar plot of gender by percentage in plotly
    author_gender_df.columns = ["Sub-Category", "Percentage"]
    fig = px.bar(
        author_gender_df,
        x="Sub-Category",
        y="Percentage",
        title="Procentul comenzilor in functie de subcategorie",
        color_discrete_sequence=["#444657"],
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Din grafic se poate observa tendinta de consum pentru fiecare subcategorie ")


with row4_2:
    st.subheader("Ce cantitate se comanda cel mai frecvent?")
    fig = px.histogram(
        df_database,
        x="Quantity",
        title="Tendinta ",
        color_discrete_sequence=["#e3a462"],
    )
    fig.update_xaxes(title_text="Cantitatea comandata")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Se poate observa care este distributia cantitatii comandate de catre clientii magazinului!"
    )

add_vertical_space()
row5_space1, row5_1, row5_space2, row5_2, row5_space3 = st.columns(
    (0.1, 1, 0.1, 1, 0.1)
)

with row5_1:
    st.subheader("Distributia pretului unitar de vanzare")
    fig = px.histogram(
        df_database,
        x="Sales",
        title="Distributia pretului de vanzare",
        color_discrete_sequence=["#4c3ca3"],
    )
    fig.update_xaxes(title_text="Pretul unitar")
    fig.update_yaxes(title_text="Count")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    book_len_avg = round(np.mean(pd.to_numeric(df_database["Sales"].dropna())))
    book_len_max = pd.to_numeric(df_database["Sales"]).max()
    row_long = df_database[pd.to_numeric(df_database["Sales"]) == book_len_max]
    longest_book = row_long["Sub-Category"].iloc[0]

    st.markdown(
        "Pretul unitar mediu este de **{}**, iar cel mai mare pret unitar de vanzare este pentru subcategoria **{} in valoare de  {}!**.".format(
            book_len_avg, longest_book, int(book_len_max)
        )
    )

with row5_2:
    st.subheader("Distributia comenzilor pe regiuni in timp")
    year_author_df = pd.DataFrame(
        df_database.groupby(["Order Date"])["Region"].value_counts(normalize=True)
    )
    year_author_df.columns = ["Percentage"]
    year_author_df.reset_index(inplace=True)
    year_author_df = year_author_df[year_author_df["Order Date"] != ""]
    year_author_df["Order Date"] = pd.to_timedelta(year_author_df["Order Date"])
    # plot line plot in plotly of year_author_df with x axis as read_at_year, y axis is percentage, color is author gender
    fig = px.line(
        year_author_df,
        x="Order Date",
        y="Percentage",
        color="Region",
        title="Procentul comenzilor in functie de regiune in timp",
    )
    fig.update_xaxes(title_text="Anul comenzii")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
    st.markdown(
        "Se poate observa procentul comenzilor in functie de fiecare regiune si cum s-a schimbat acesta in timp."
    )
add_vertical_space()
row7_spacer1, row7_1, row7_spacer2 = st.columns((0.1, 3.2, 0.1))

st.markdown("***")
st.markdown(
        "Multumesc pentru ca ati parcurs aceasta analiza! Apreciez feedbaack- ul, si daca doriti sa stiti mai multe ma puteti gasi pe [website](https://lauracarpaciu.github.io) ")

