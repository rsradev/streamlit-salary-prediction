import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorten_categories(categories, cutoff):
    cat_map = {}
    for c in range(len(categories)):
        if categories.values[c] >= cutoff:
            cat_map[categories.index[c]] = categories.index[c]
        else:
            cat_map[categories.index[c]] = 'Other'
    return cat_map


def clean_expr(x):
    if x == 'More than 50 years':
        return 50
    elif x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return "Bachelor's degree"
    elif 'Master’s degree' in x:
        return "Master's degree"
    elif 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache_resource
def load_data():
    df = pd.read_csv(
        './data/survey_results_public.csv'
    )
    df = df[
        [
            'Country',
            'EdLevel',
            'YearsCodePro',
            'Employment',
            'ConvertedCompYearly'
        ]
    ]
    df = df.rename({'ConvertedCompYearly': 'Salary'}, axis=1)
    df = df[df['Salary'].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == 'Employed, full-time']
    df = df.drop('Employment', axis=1)
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df['Salary'] <= 250_000]
    df = df[df['Salary'] >= 10_000]
    df = df[df['Salary'] != 'Other']
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_expr)
    df['EdLevel'] = df['EdLevel'].apply(clean_edu)

    return df


df = load_data()


def show_explore_page():
    st.title('Explore Software Engineer`s Salary')
    st.write(
        """
            #### Based on Stack Overflow Developer Survey 2023
        """
    )

    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(
        data,
        labels=data.index,
        autopct="%1.1f%%",
        shadow=True,
        startangle=900
    )
    ax1.axis('equal')

    st.write("""
             #### Countries
             """)
    st.pyplot(fig1)

    st.write(
        """
        ### Mean Salary per country
        """
    )

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
        ### Mean Salary based on experience(years)
        """
    )

    data = df.groupby(
        ['YearsCodePro']
    )['Salary'].mean().sort_values(ascending=True)

    st.line_chart(data)