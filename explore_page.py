import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache_data
def shorten(categories, cutoff):
    cat_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            cat_map[categories.index[i]] = categories.index[i]
        else:
            cat_map[categories.index[i]] = "Others"
    return cat_map

def clean_edu(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x: 
        return 'Pstgrad'
    return 'Less than a Bachelors'
    
def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def load_data():
    data = pd.read_csv('survey_results_public.csv')
    pd.set_option("display.max_columns", None)
    data = data[['Country', "EdLevel", "YearsCode", "Employment", "ConvertedCompYearly"]]
    data = data.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    data = data[data["Salary"].notnull()]
    data = data.dropna()
    data = data[data['Employment'] == "Employed, full-time"]
    data = data.drop("Employment", axis=1)
    country_map = shorten(data.Country.value_counts(), 400)
    data["Country"] = data["Country"].map(country_map)
    data = data[data['Salary'] <= 500000]
    data = data[data['Salary'] >= 100000]
    data = data[data['Country'] != 'Others']
    data['YearsCode'] = data['YearsCode'].apply(clean_experience)
    data['EdLevel'] = data['EdLevel'].apply(clean_edu)

    return data

data = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")
    st.write("""### Stack Overflow Developer Survey 2023""")

    df = data['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(df, labels=df.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis('equal')

    st.write("""#### Number of data from different countries""")
    st.pyplot(fig1)

    st.write("""#### Mean Salary Based on Country""")
    df=data.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(df)

    st.write("""#### Mean Salary Based on Experience""")

    df=data.groupby(['YearsCode'])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(df)

    
show_explore_page()
