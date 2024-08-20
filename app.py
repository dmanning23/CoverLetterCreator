import os
from keys import openAIapikey
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import (SystemMessage, HumanMessage)

def main():
    os.environ["OPENAI_API_KEY"] = openAIapikey
    st.set_page_config(
        page_title="Create A Cover Letter",
        page_icon="📜")

    container = st.container()
    with container:
        with st.form(key="my form", clear_on_submit=False):

            #Allow the user to provide a job description
            jobPost  = st.text_area(label="Copy/Paste the job post: ", key="jobPost", height = 200)

            #Allow the user to provide a resume:
            resume  = st.text_area(label="Copy/Paste your resume: ", key="resume", height = 200)
            
            #Add a button to generate the cover letter
            submit_button = st.form_submit_button(label="Create Cover Letter!")

        if submit_button:

            #Check that a job post was provided
            if not jobPost:
                st.error("Job description is missing")

            #Check that a resume was provided
            if not resume:
                st.error("Resume is missing")

            if jobPost and resume:
                with st.spinner("Thinking..."):
                    llm = ChatOpenAI(temperature=0.3) #run the LLM slightly chilled to prevent hallucinations
                    messages = [
                        SystemMessage(content="Provided are a job description and a resume. Assume you are the candidate described in the resume. Write a cover letter for the position described in the job post. Try to line up the requirements in the job post with experience from the resume, and emphasize leadership capabilities."),
                        SystemMessage(content="Make sure your response is in markdown format."),
                        HumanMessage(content=f"Job description: {jobPost}"),
                        HumanMessage(content=f"Resume: {resume}"),]
                    result = llm.invoke(messages)
            
                #Display the ressponse to the user
                st.markdown(f"{result.content}")
    
if __name__ == "__main__":
    main()