import streamlit as st
import pickle 
import numpy as np

def load_model():
    with open('save_steps.pkl','rb') as file:
         df = pickle.load(file)
    return df

df = load_model()

reg = df['model']
le_country = df['le_country']
le_education = df['le_education']

def show_pred_page():
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict salary""")

    countries = {
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
        'Israel', 
    }

    education = {
        'Bachelor’s degree',
        'Master’s degree',
        'Postgrad',
        'Less than a Bachelors',
    }

    country = st.selectbox("Country", list(countries))
    edu = st.selectbox("Education Level", list(education))
    experience = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button('Calculate Salary')
    if ok:
        X = np.array([[country, edu, experience]])
        X[:, 0] = le_country.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = reg.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")

