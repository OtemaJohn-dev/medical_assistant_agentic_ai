import streamlit as st 
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from dotenv import dotenv_values

config = dotenv_values(".env")

if "llm" not in st.session_state:
    llm = ChatGroq(
        model=config["GROQ_API_MODEL"],
        api_key=config["GROQ_API_KEY"],
        temperature=0.1,
        max_tokens=131_072,
    )
    st.session_state.llm = llm
else:
    llm = st.session_state.llm

    system_message = SystemMessage(
        content = """You are a helpful assistant, 
        you provide response to the doctor, Patients, Pharmacy 
        while considering AI ethics 
        in such a way that you don't provide dangerous response to the users that can be dangerous to the health"""
    )

st.title("AI AGENTIC MEDICAL ASSISTANT")

st.write("This is a simple Streamlit app for an AI Agentic Medical Assistant.")

role = st.sidebar.selectbox(
    "Select Role",
    ["Administrator", "Doctor", "Patient", "Pharmacist"]
)
st.image("screenshots/medical_assistant.jpg", caption="Agent Doctors")

if role == "Administrator":
    st.header("Administrator Dashboard")

elif role == "Doctor":
    st.header("PATIENTS BIO-DATA")
    st.text_input("Patients name: ")
    st.text_input("Patients age: ")
    st.text_input("Patients id_number: ")
    st.text_input("Patients password: ")

    st.button("Submit Patients Bio-Data", type="primary")
    if st.button == "clicked":
        st.write("Data saved successfully")
    else:
        st.write("Data not saved! Please try again")

    st.header("PATIENTS DIAGNOSIS")
    st.text_area("Patients complaints: ")
    st.text_area("Patients suggested medication: ")
    st.text_area("Doctors Advise to the patient: ")

    st.button("Submit Patients Diagnosis", type="primary")
    if st.button == "clicked":
        st.write("Patient diagnosis saved successfully")
    else:
        st.write("Patient diagnosis not saved! Please try again")



        st.header("Doctor, Talk to the AI Agent Assistant incase of a new diagnosis")

        if "message_1" not in st.session_state:
            st.session_state.message_1 = [system_message]


        def get_doctor_response():
            messages = st.session_state.message_1
            response = llm.invoke(messages)
            st.session_state.message_1.append(response)
            return response
            
        for message in st.session_state.message_1:
            if isinstance(message, HumanMessage):
                with st.chat_message("user"):            
                    st.write(message.content)
            elif isinstance(message, AIMessage):
                with st.chat_message("assistant"):
                    st.write(message.content)
                
        
        if msgs := st.chat_input("Describe a new symptom and complaints"):
            st.session_state.message_1.append(HumanMessage(content=msgs))
            response = get_doctor_response()
            st.rerun()




elif role == "Patient":
    st.header("Patients inquiry form")

    if "message" not in st.session_state:
        st.session_state.message = [system_message]

    for message in st.session_state.message:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    def get_response():
        messages = st.session_state.message
        response = llm.invoke(messages)
        st.session_state.message.append(response)
        return response

    if msgs := st.chat_input("Enter your message here"):
        st.session_state.message.append(HumanMessage(content=msgs))
        response = get_response()
        st.rerun()

elif role == "Pharmacist":
    st.header("Pharmacist Dashboard")
    st.image("screenshots/AAR-Pharmacy.jpg", caption="Pharmacist")

    st.header("Add available Drugs")

    st.text_input("Drug name: ")
    st.text_input("Drug description: ")
    st.text_input("Drug price: ")
    st.text_input("Drug quantity: ")
    st.text_input("Drug manufacturer: ")
    st.text_input("Drug category: ")
    st.text_input("Drug brand: ")

    st.button("Add Drug", type="primary")
    if st.button == "clicked":
        st.write("Drug added successfully")
    else:
        st.write("Drug not added! Please try again")


    st.header("Pharmacist, Talk to the AI Agent Assistant incase of a new drug")


    if "message_2" not in st.session_state:
        st.session_state.message_2 = [system_message]

    for message in st.session_state.message_2:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    def get_pharmacist_response():
        messages = st.session_state.message_2
        response = llm.invoke(messages)
        st.session_state.message_2.append(response)
        return response


    if msgs := st.chat_input("Enter your message here"):
        st.session_state.message_2.append(HumanMessage(content=msgs))
        response = get_pharmacist_response()
        st.rerun()


