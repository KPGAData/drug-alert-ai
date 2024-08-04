from data import drugs, doctors_data, doctors_df
from workflows import DrugWorkflow
from workflows import STATE_GENERATION, STATE_DOWNLOAD_HCP_DATA, STATE_AI_PROCESSING, STATE_GENERATE_TEMPLATES, STATE_TEMPLATES_READY
from workflows import STATE_APPROVALS, STATE_MEDICAL_APPROVAL, STATE_COMPLIANCE_APPROVAL, STATE_BRAND_APPROVAL, STATE_TEMPLATES_APPROVED
from workflows import STATE_DISTRIBUTION, STATE_FIND_TARGET_DOCTORS, STATE_GENERATE_TAILORED_COMMS, STATE_SEND_COMMUNICATION, STATE_DISTRIBUTED
from ai import AI
from graph_data import generate_graph_data
from dotenv import load_dotenv
from uuid import uuid4
import os
import streamlit as st
from streamlit_react_flow import react_flow
from file_utils import get_file_type
from PIL import Image
import sys
import pandas as pd
import PyPDF2

# Configure
st.set_page_config(page_title="DDD", layout="wide")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = f"AIE3 - LangGraph - {uuid4().hex[0:8]}"

print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Initialize
load_dotenv()

@st.cache_resource
def load_ai() -> AI:
    ai = AI()
    ai.load_model()
    ai.load_embeddings()
    ai.load_tools()
    print (ai.model)
    return ai

ai = load_ai()

@st.cache_resource
def load_workflows():
    workflows = {}
    all_workflow = DrugWorkflow({"name":"All", "company":"All"}, ai)
    all_workflow.load_workflow()
    workflows["All"] = all_workflow
    for drug in drugs:
        workflow = DrugWorkflow(drug, ai) 
        workflow.load_workflow()
        # workflow.start_workflow()
        workflows[drug["name"]] = workflow
    return workflows

workflows = load_workflows()

def dump_session_state():
    print("### Session State Dump")
    for key, value in st.session_state.items():
        print(f"{key}: {value}")

dump_session_state()

selected_drug = "All"
selected_doctor = "All"

if "selected_drug" in st.session_state:
    selected_drug = st.session_state["selected_drug"]

if "selected_doctor" in st.session_state:
    selected_doctor = st.session_state["selected_doctor"]

print("Selected Drug : " + selected_drug)
print("Selected Doctor : " + selected_doctor)

st.markdown("# Drug Alert AI")
st.markdown("---")

if selected_drug=="All":
    _, col, _ = st.columns(3)
    with col:
        st.subheader("Reference Workflow")
else:
    _, col, _ = st.columns(3)
    with col:
        st.subheader("Workflow for " + selected_drug)


flowStyles = { "height": 500,"width":"100%" }
elements = generate_graph_data(workflows[selected_drug])

flow = react_flow("DDD",elements=elements,flow_styles=flowStyles)

workflow = workflows[selected_drug]

def run_graph():
    workflow.start_workflow()

def resume_graph():
    workflow.resume_workflow()

def stop_graph():
    workflow.stop_workflow()

def show_preview(file_path):
    file_type = get_file_type(file_path)
    file = open(file_path, "r")
    print(f"file_type {file_type}")
    if "image" in file_type:
        image = Image.open(file)
        st.image(image, width=300)
    elif "pdf" in file_type:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[0]
        st.text(page.extract_text()[:500] + "...")  # Show first 500 characters
    elif "txt" in file_type:
        st.text_area("", file.read(), height=2000)
    elif "text" in file_type:
        st.text_area("", file.read(), height=2000)
    elif "html" in file_type:
        st.html(file.read())
    elif "spreadsheet" in file_type:
        df = pd.read_csv(file)  # Assuming CSV, adjust for Excel if needed
        st.dataframe(df.head(), width=600, height=200)
    file.close()

if selected_drug != "" "All":
    workflow = workflows[selected_drug]
    current_state = workflow.current_state()

    file_path = f"data/output/generated/{selected_drug}.txt"
    if not workflow.is_active():
        _, col, _ = st.columns(3)
        with col:
            st.markdown(f"""<h3 style='color: red;'>Workflow has stopped</h3>""", unsafe_allow_html=True)
        # st.markdown(
        #     f"""
        #     <div style='text-align: center; font-size: 35px;'>
        #         {msg}
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        #)
    elif current_state == STATE_APPROVALS:
        _, col3, _ = st.columns(3)
        with col3:
            st.markdown(f"""<h3 style='text-align: center;'>Medical Approval</h1>""", unsafe_allow_html=True)
            st.markdown(f"""<h3 style='color: green; text-align: center;'>Approve ?</h1>""", unsafe_allow_html=True)
        _, _, _, _, _, col2, col3, _, _, _, _, _ = st.columns(12)
        with col2:
            st.button(":white_check_mark:", key="medical_approved", on_click=resume_graph)
        with col3:
            st.button(":o2:", key="medical_declined", on_click=stop_graph)
        show_preview(file_path)
    elif current_state == STATE_MEDICAL_APPROVAL:
        _, col3, _ = st.columns(3)
        with col3:
            st.markdown(f"""<h3 style='text-align: center;'>Compliance Approval</h1>""", unsafe_allow_html=True)
            st.markdown(f"""<h3 style='color: green; text-align: center;'>Approve ?</h1>""", unsafe_allow_html=True)
        _, _, _, _, _, col2, col3, _, _, _, _, _ = st.columns(12)
        with col2:
            st.button(":white_check_mark:", key="compliance_approved", on_click=resume_graph)
        with col3:
            st.button(":o2:", key="compliance_declined", on_click=stop_graph)
        show_preview(file_path)
    elif current_state == STATE_COMPLIANCE_APPROVAL:
        _, col3, _ = st.columns(3)
        with col3:
            st.markdown(f"""<h3 style='text-align: center;'>Brand Approval</h1>""", unsafe_allow_html=True)
            st.markdown(f"""<h3 style='color: green; text-align: center;'>Approve ?</h1>""", unsafe_allow_html=True)
        _, _, _, _, _, col2, col3, _, _, _, _, _ = st.columns(12)
        with col2:
            st.button(":white_check_mark:", key="brand_approved", on_click=resume_graph)
        with col3:
            st.button(":o2:", key="brand_declined", on_click=stop_graph)
        show_preview(file_path)
    elif current_state == STATE_GENERATE_TAILORED_COMMS:
        _, col3, _ = st.columns(3)
        with col3:
            st.markdown(f"""<h3 style='text-align: center;'>Review Communication</h1>""", unsafe_allow_html=True)
            st.markdown(f"""<h3 style='color: green; text-align: center;'>Send ?</h1>""", unsafe_allow_html=True)
        _, _, _, _, _, col2, col3, _, _, _, _, _ = st.columns(12)
        with col2:
            st.button(":white_check_mark:", key="email_approved", on_click=resume_graph)
        with col3:
            st.button(":o2:", key="email_declined", on_click=stop_graph)
        file_path = f"data/output/email/{selected_drug}.html"
        show_preview(file_path)
    else:
        # Define custom CSS for button colors
        button_style = """
        <style>
            .stButton > button {
                color: white;
                background-color: #4CAF50;
                border-radius: 5px;
            }
            .stButton > button:hover {
                background-color: #45a049;
            }
            .red-button > button {
                background-color: #f44336;
            }
            .red-button > button:hover {
                background-color: #da190b;
            }
        </style>
        """
        st.markdown(button_style, unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col3:
            st.button("Run", key="run_graph", on_click=run_graph)

# st.markdown("### Drugs")
# st.markdown(">")

# md = "| "
# for drug in drugs:
#     md = md + (f'**[{drug["name"]}]({drug["link"]})** | ')

# st.markdown(md)

def doctors():
    st.subheader("Doctors")
    st.dataframe(doctors_df, use_container_width=True, height=800)

def go_to_doctors_page():
    doctors_page = st.navigation([
        st.Page(doctors, title="Doctors")
    ])
    doctors_page.run()

# go_to_doctors_page()

def on_drug_change():
    print("You selected drug : ", st.session_state.selected_drug)

def on_doctor_change():
    print("You selected doctor : ", st.session_state.selected_doctor)

with st.sidebar:
    st.image(Image.open("logo.png"), use_column_width=True)

    st.title("Drugs")
    drug_list = ["All"]
    for drug in drugs:
        name = drug["name"]
        drug_list.append(name)
    selected_drug = st.selectbox("", drug_list, key="selected_drug", on_change=on_drug_change)

    st.write("")
    st.title("Doctors")
    doctor_list = ["All"]
    for doctor in doctors_data:
        name = doctor["Name"] 
        doctor_list.append(name)
    selected_doctor = st.selectbox("", doctor_list, key="selected_doctor", on_change=on_doctor_change)