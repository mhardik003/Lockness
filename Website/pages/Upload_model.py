import streamlit as st

st.set_page_config(
    page_title="Lockness",
    page_icon="🔒",
    layout="wide",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Lockness is a platform that allows you to upload your data and machine learning models to keep them safe."
    }
)


st.header("Upload Your Encrypted Model Here")

new_model_name = st.text_input("Enter the name of your model here")
new_model = st.file_uploader("Upload your model here")

if new_model:
    st.write(f'Your model has been uploaded successfully as "{new_model_name}"!')
    with open('models.txt', 'a') as f:
        f.write(f'{new_model_name}\n')
        
    f.close()