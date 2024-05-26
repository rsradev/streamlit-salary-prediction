import streamlit as st
import pickle 
import numpy as np


def load_modulue():
    with open('./data/steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_modulue()

regressor = data['model']
le_country = data['le_country']
le_education = data['le_education']


def show_predict_page():
    st.title('Software Developer Salary Prediction')

    st.write(
        """
    #### information for the prediction
        """
    )

    countries = (
        'United States of America',
        'Germany',
        'United Kingdom of Great Britain and Northern Ireland',
        'Canada',
        'India',
        'France',
        'Netherlands',
        'Australia',
        'Brazil',
        'Spain',
        'Sweden',
        'Italy',
        'Poland',
        'Switzerland',
        'Denmark',
        'Norway',
        'Israel'
    )

    education = (
        "Bachelor's degree",
        "Master's degree",
        'Post grad',
        'Less than a Bachelors'
    )

    country = st.selectbox(
        'Country:',
        countries
    )

    education = st.selectbox(
        'Degree',
        education
    )

    experience = st.slider(
        'Experience (Years):',
        0,
        50,
        3
    )

    ok = st.button('Predict Salary')
    if ok:
        X = np.array([[country, education, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f'The estimated salary is {salary[0]:.3f} $ per year')
