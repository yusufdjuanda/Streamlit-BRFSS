# Front-end 
import pandas as pd
import streamlit as st
from function import *
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie

st.set_page_config(layout="wide", page_title="BRFSS", page_icon="📑")
import json
st.set_page_config(layout="wide")

@st.cache()
def get_display_df():
    display_df = pd.read_csv(
        "brfss_original.csv",
        sep=",",
        nrows=20,
    )
    return display_df

# Creating a function to load the transformed dataset
@st.cache() # Decorator from streamlit to keep the returned function in the cache
def get_df():
    df = pd.read_csv("BRFSS.csv", sep=",")
    df['Category'] = df['Category'].str.replace(", non-Hispanic","")
    df['Year'] = df['Year'].astype('str')
    df['Response'] = df['Response'].str.replace("bmi","BMI")
    return df

# Creating a function to load the location dataset
@st.cache()
def get_loc_df():
    df_loc = pd.read_csv("brfss_smokers.csv", sep = ",")
    return df_loc

# Creating function to load icon file 
@st.cache()
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

   

display_df = get_display_df()
transformed_df = get_df()
loc_df = get_loc_df()



with st.sidebar:
    selected = option_menu(
        menu_title = None,
        options = ['About the Project',"---", 'BRFSS', 'Smoking Status'],
        styles={
        "icon": {"font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"1px"},
        },
        icons=['house', None, 'card-checklist', 'clipboard-data'], 
        menu_icon="cast", default_index=0
    )
    

if selected == 'About the Project':
    filepath = "employee-getting-customer-requirements.json"
    lottie_json = load_lottiefile(filepath)
    st_lottie(lottie_json,height = 300, width = 300)
    main_page()
if selected == 'BRFSS':
    st.image("BRFSS.png", width=250)
    filepath = "form.json"
    lottie_json = load_lottiefile(filepath)
    brfss_page(display_df, transformed_df, loc_df, lottie_json)
if selected == 'Smoking Status':
    filepath = "smoking.json"
    lottie_json = load_lottiefile(filepath)
    st_lottie(lottie_json,height = 100, width = 100)
    smoking_page(transformed_df, loc_df)

