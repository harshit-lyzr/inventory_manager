import os
from lyzr import DataAnalyzr
from dotenv import load_dotenv
import streamlit as st
from utils import save_uploaded_file
from PIL import Image

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

load_dotenv()
api = os.getenv('OPENAI_API_KEY')

data = "data"
os.makedirs(data, exist_ok=True)


def style_app():
    # You can put your CSS styles here
    st.markdown("""
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """, unsafe_allow_html=True)

    image = Image.open("lyzr-logo.png")
    st.image(image, width=150)

    st.title("Lyzr Inventory Manager")
    st.markdown("You Have upload Your Inventory CSV File and Enter Your Query.It will Generate Insights,Recommendations and Tasks for You to manage Inventory.")


def data_uploader():
    st.subheader("Upload Data file")
    # Upload csv file
    uploaded_file = st.file_uploader("Choose csv file", type=["csv"])
    if uploaded_file is not None:
        save_uploaded_file(uploaded_file)


def file_checker():
    file = []
    for filename in os.listdir(data):
        file_path = os.path.join(data, filename)
        file.append(file_path)

    return file


def inventory_manager(path, question):
    analyzr = DataAnalyzr(analysis_type="sql", api_key=api)
    datafiles = {
        "test1": path,

    }
    # Call the get_data method
    analyzr.get_data(
        db_type = "files",
        config = {
                "datasets": datafiles,
        },
        vector_store_config = {}
    )

    result = analyzr.ask(
        user_input = f"you are an inventory manager.Your Task is to Give Answer for Question from given Dataset: {question}",
        outputs=["insights","recommendations","tasks"]
    )

    return result


if __name__ == "__main__":
    style_app()
    st.sidebar.markdown("## Welcome to the Lyzr Inventory Manager!")
    selection = st.sidebar.radio("Go to", ["Data", "Analysis"])

    if selection == "Data":
        data_uploader()
    elif selection == "Analysis":
        file = file_checker()
        if len(file) > 0:
            questions = st.text_input("Enter Your Question: ")
            if st.button("Generate"):
                answer = inventory_manager(file[0], questions)
                st.markdown("## Insights")
                st.markdown(answer['insights'])
                st.markdown("## Recommendations: ")
                st.markdown(answer['recommendations'])
                st.markdown("## Tasks:")
                st.markdown(answer['tasks'])

