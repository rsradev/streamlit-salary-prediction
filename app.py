import streamlit as st
from predict import show_predict_page
from explore import show_explore_page

page = st.sidebar.selectbox(
    'Explore or Predict',
    ('Prediction', 'Exploration')
)

if page == 'Prediction':
    show_predict_page()
elif page == 'Exploration':
    show_explore_page()
