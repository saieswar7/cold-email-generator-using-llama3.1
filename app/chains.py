import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("groq_api_key")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            groq_api_key = groq_api_key,
            temperature=0.6,
            model="llama-3.1-70b-versatile"
        )
    
    def extract_jobs(self,scrapedata):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the careers's page of a website.
            your job is to extract the job postings and return then in JSON format containing the following
            keys :`role`,`experience`,`skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data",scrapedata})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except Exception:
            print("Context is too big")
    
        return res if isinstance(res,list) else [res]
    
    
    def generate_cold_email(self,job,links):
        
        prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION
                {job_description}
                ### INSTRUCTION:
                You are Sai, a business development executive at TCS. TCS is an AI & Software consultive company
                dedicated and provide the seamless integration of business process through automated tools.
                Over our experience, we have empowered numerous enterprises with tailored solutions, foestering the 
                process optimization, cost reduction, and heightened overall efficiency.
                Your job is to write a cold email to the client regarding the job mentioned above describing what we do
                and how we help in fulfilling their needs.
                Also add the most revelevant ones from the following links to showcase TCS portfolio:{link_list}
                Remember you are Sai, BDE at TCS.
                Do not provide any preamble
                ### EMAIL (NO PREAMBLE):
                """
        )
        chain_extract = prompt_email | self.llm
        res = chain_extract.invoke(input={"job_description":str(job),"link_list":links})
        return res.content
    
            
        