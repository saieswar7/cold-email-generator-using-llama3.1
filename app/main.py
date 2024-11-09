import streamlit as st

from portfolio import Portfolio
from chains import Chain
from utils import clean_text

from langchain_community.document_loaders import WebBaseLoader


def create_streamlit_app(llm,portfolio,clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter a URL",value="https://www.livehire.com/careers/nikeinc/job/PX8XT/6KZB7QZSLP/data-engineer-manager")
    submit_button = st.button("Submit")
    if submit_button:
            loader = WebBaseLoader(url_input)
            data = clean_text(loader.load().pop().page_content)
            print(data)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            skills = jobs[0].get('skills',[])
            links = portfolio.query_links(skills)
            email = llm.generate_cold_email(jobs,links)
            st.code(email,language="markdown")
if __name__=="__main__":
    llm = Chain()
    Portfolio = Portfolio()
    create_streamlit_app(llm,Portfolio,clean_text)
        