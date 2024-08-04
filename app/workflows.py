import random
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from ai import AI
from langgraph.prebuilt import ToolInvocation
from langchain_core.messages import FunctionMessage
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from utils import generate_random_phone_number
from data import doctors_data
from PIL import Image
import json
import os
import ssl
import markdown
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MSG_CONTINUE = "continue"
MSG_END = "END"

STATE_GENERATION = "Generation"
STATE_DOWNLOAD_HCP_DATA = "Download HCP Data"
STATE_AI_PROCESSING = "AI Processing"
STATE_GENERATE_TEMPLATES = "Generate templates"
STATE_TEMPLATES_READY = "Templates Ready"
STATE_APPROVALS = "Approvals"
STATE_MEDICAL_APPROVAL = "Medical Approval"
STATE_COMPLIANCE_APPROVAL = "Compliance Approval"
STATE_BRAND_APPROVAL = "Brand Approval"
STATE_TEMPLATES_APPROVED = "Templates Approved"
STATE_DISTRIBUTION = "Distribution"
STATE_FIND_TARGET_DOCTORS = "Find Target Doctors"
STATE_GENERATE_TAILORED_COMMS = "Target Communication"
STATE_SEND_COMMUNICATION = "Send Communication"
STATE_DISTRIBUTED = "Distributed"

states = [STATE_GENERATION, STATE_DOWNLOAD_HCP_DATA, STATE_AI_PROCESSING, STATE_GENERATE_TEMPLATES, STATE_TEMPLATES_READY,
STATE_APPROVALS, STATE_MEDICAL_APPROVAL, STATE_COMPLIANCE_APPROVAL, STATE_BRAND_APPROVAL, STATE_TEMPLATES_APPROVED,
STATE_DISTRIBUTION, STATE_FIND_TARGET_DOCTORS, STATE_GENERATE_TAILORED_COMMS, STATE_SEND_COMMUNICATION, STATE_DISTRIBUTED]

num_states = len(states)

print(f'Initiliazed {num_states} states')

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

class StateMachine():
    def __init__(self) -> None:
        self.machine = {}
        self.current_state = None

    def record_state(self, state):
        self.current_state = state
        self.machine[state] = 1

    def isStateDone(self, state) -> bool:
        return self.machine.get(state) is not None
    
    def current_state(self):
        return self.current_state

class Drug:
    def __init__(self, drug) -> None:
        self.Name = drug["name"]
        self.Link = drug["link"]
        self.Company = drug["company"]

class DrugWorkflow:
    def __init__(self, drug, AI) -> None:
        self.AI = AI
        self.graph = None
        self.drug = drug
        self.thread = None
        self.active = True
        self.html_content = None
        self.state_machine = StateMachine()

    def is_active(self):
        return self.active

    def current_state(self):
        return self.state_machine.current_state

    def html_content(self):
        return self.html_content

    def generation(self, state):
        self.state_machine.record_state(STATE_GENERATION)
        print(STATE_GENERATION + " step done for " + self.drug["name"])
        pass

    ### Data Preparation Step. Download PDF file and website content as needed. If content already exists, then skip
    def drug_hcp_site(self, state) -> str:
        self.AI.loadDrugData(self)        
        self.state_machine.record_state(STATE_DOWNLOAD_HCP_DATA)
        print(STATE_DOWNLOAD_HCP_DATA + " step done for " + self.drug["name"])
        pass

    ### Retrieval Step. Embedding. Store. 
    def ai_processing(self, state) -> str:
        self.AI.retrieveAndCreateEmbeddingStore()  
        self.state_machine.record_state(STATE_AI_PROCESSING)
        print(STATE_AI_PROCESSING + " step done for " + self.drug["name"])
        pass

    ### Generation Step. Prepare context. Prompt. 
    def generate_templates(self, state) -> str:
        self.AI.createPrompt(self)
        self.state_machine.record_state(STATE_GENERATE_TEMPLATES)
        print(STATE_GENERATE_TEMPLATES + " step done for " + self.drug["name"])
        pass

    ### Get the output from AI and generate template files into templates/generated folder
    def templates_ready(self, state) -> str:
        self.AI.generateTempleteFromAI(self)  
        self.state_machine.record_state(STATE_TEMPLATES_READY)
        print(STATE_TEMPLATES_READY + " step done for " + self.drug["name"])
        pass

    def approvals(self, state) -> str:
        self.state_machine.record_state(STATE_APPROVALS)
        print(STATE_APPROVALS + " step done for " + self.drug["name"])
        pass

    def medical_approval(self, state) -> str:
        self.state_machine.record_state(STATE_MEDICAL_APPROVAL)
        print(STATE_MEDICAL_APPROVAL + " step done for " + self.drug["name"])
        pass

    def compliance_approval(self, state) -> str:
        self.state_machine.record_state(STATE_COMPLIANCE_APPROVAL)
        print(STATE_COMPLIANCE_APPROVAL + " step done for " + self.drug["name"])
        pass

    def brand_approval(self, state) -> str:
        self.state_machine.record_state(STATE_BRAND_APPROVAL)
        print(STATE_BRAND_APPROVAL + " step done for " + self.drug["name"])
        pass

    def templates_approved(self, state) -> str:
        self.state_machine.record_state(STATE_TEMPLATES_APPROVED)
        print(STATE_TEMPLATES_APPROVED + " step done for " + self.drug["name"])
        pass

    def distribution(self, state) -> str:
        self.state_machine.record_state(STATE_DISTRIBUTION)
        print(STATE_DISTRIBUTION + " step done for " + self.drug["name"])
        pass

    def find_target_doctors(self, state) -> str:
        self.state_machine.record_state(STATE_FIND_TARGET_DOCTORS)
        print(STATE_FIND_TARGET_DOCTORS + " step done for " + self.drug["name"])
        pass


    def generate_tailored_comms(self, state) -> str:
        self.state_machine.record_state(STATE_GENERATE_TAILORED_COMMS)
        drug_name = self.drug["name"]
        with open(f"data/output/generated/{drug_name}.txt", 'r') as file:
            md_content = file.read()
        self.html_content = markdown.markdown(md_content)

        hcp_count = len(doctors_data)
        hcp1 = doctors_data[random.randint(0,hcp_count-1)]
        hcp2 = doctors_data[random.randint(0,hcp_count-1)]
        self.html_content = self.html_content.replace("[Variable HCP Name]", hcp1["Name"])
        self.html_content = self.html_content.replace("[Variable Rep Name]", hcp2["Name"])
        self.html_content = self.html_content.replace("[Variable Phone Number]", generate_random_phone_number())
        self.html_content = self.html_content.replace("[Variable Rep Email]", hcp2["email_address"])

        with open(f"data/output/email/{drug_name}.html", 'w') as file:
            file.write(self.html_content)
            file.close()

        print(STATE_GENERATE_TAILORED_COMMS + " step done for " + self.drug["name"])
        pass

    def send_communication(self, state) -> str:
        self.state_machine.record_state(STATE_SEND_COMMUNICATION)
        drug_name = self.drug["name"]

        SMTP_FROM = os.environ["SMTP_FROM"]
        SMTP_TO = os.environ["SMTP_TO"]
        SMTP_SERVER = os.environ["SMTP_SERVER"]
        SMTP_PORT = os.environ["SMTP_PORT"]
        SMTP_USER = os.environ["SMTP_USER"]
        SMTP_PASS = os.environ["SMTP_PASS"]

        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"Latest drug information"
        msg['From'] = SMTP_FROM
        msg['To'] = SMTP_TO

        # Attach the HTML content
        html_part = MIMEText(self.html_content, 'html')
        msg.attach(html_part)

        # Send the email
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls(context=context)
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")
    
        print(STATE_SEND_COMMUNICATION + " step done for " + self.drug["name"])
        pass

    def distributed(self, state) -> str:
        self.state_machine.record_state(STATE_DISTRIBUTED)
        print(STATE_DISTRIBUTED + " step done for " + self.drug["name"])
        print("Last state of the workflow. Exiting.")
        self.active = False
        pass

    def should_continue(state):
        last_message = state["messages"][-1]

        if "function_call" not in last_message.additional_kwargs:
            return MSG_END

        return MSG_CONTINUE

    def call_model(self, state) -> dict:
        messages = state["messages"]
        response = self.AI.model.invoke(messages)
        return {"messages" : [response]}

    def call_tool(self, state) -> dict:
        last_message = state["messages"][-1]

        action = ToolInvocation(
            tool=last_message.additional_kwargs["function_call"]["name"],
            tool_input=json.loads(
                last_message.additional_kwargs["function_call"]["arguments"]
            )
        )

        response = self.AI.tool_executor.invoke(action)

        function_message = FunctionMessage(content=str(response), name=action.tool)

        return {"messages" : [function_message]}

    def load_workflow(self):
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node(STATE_GENERATION, self.generation)
        graph_builder.add_node(STATE_DOWNLOAD_HCP_DATA, self.drug_hcp_site)
        graph_builder.add_node(STATE_AI_PROCESSING, self.ai_processing)
        graph_builder.add_node(STATE_GENERATE_TEMPLATES, self.generate_templates)
        graph_builder.add_node(STATE_TEMPLATES_READY, self.templates_ready)
        graph_builder.add_node(STATE_APPROVALS, self.approvals)
        graph_builder.add_node(STATE_MEDICAL_APPROVAL, self.medical_approval)
        graph_builder.add_node(STATE_COMPLIANCE_APPROVAL, self.compliance_approval)
        graph_builder.add_node(STATE_BRAND_APPROVAL, self.brand_approval)
        graph_builder.add_node(STATE_TEMPLATES_APPROVED, self.templates_approved)
        graph_builder.add_node(STATE_DISTRIBUTION, self.distribution)
        graph_builder.add_node(STATE_FIND_TARGET_DOCTORS, self.find_target_doctors)
        graph_builder.add_node(STATE_GENERATE_TAILORED_COMMS, self.generate_tailored_comms)
        graph_builder.add_node(STATE_SEND_COMMUNICATION, self.send_communication)
        graph_builder.add_node(STATE_DISTRIBUTED, self.distributed)

        graph_builder.add_edge(STATE_GENERATION, STATE_DOWNLOAD_HCP_DATA)
        graph_builder.add_edge(STATE_DOWNLOAD_HCP_DATA, STATE_AI_PROCESSING)
        graph_builder.add_edge(STATE_AI_PROCESSING, STATE_GENERATE_TEMPLATES)
        graph_builder.add_edge(STATE_GENERATE_TEMPLATES, STATE_TEMPLATES_READY)
        graph_builder.add_edge(STATE_TEMPLATES_READY, STATE_APPROVALS)
        graph_builder.add_edge(STATE_APPROVALS, STATE_MEDICAL_APPROVAL)
        graph_builder.add_edge(STATE_MEDICAL_APPROVAL, STATE_COMPLIANCE_APPROVAL)
        graph_builder.add_edge(STATE_COMPLIANCE_APPROVAL, STATE_BRAND_APPROVAL)
        graph_builder.add_edge(STATE_BRAND_APPROVAL, STATE_TEMPLATES_APPROVED)
        graph_builder.add_edge(STATE_TEMPLATES_APPROVED, STATE_DISTRIBUTION)
        graph_builder.add_edge(STATE_DISTRIBUTION, STATE_FIND_TARGET_DOCTORS)
        graph_builder.add_edge(STATE_FIND_TARGET_DOCTORS, STATE_GENERATE_TAILORED_COMMS)
        graph_builder.add_edge(STATE_GENERATE_TAILORED_COMMS, STATE_SEND_COMMUNICATION)
        graph_builder.add_edge(STATE_SEND_COMMUNICATION, STATE_DISTRIBUTED)

        graph_builder.add_edge(STATE_DISTRIBUTED, END)

        graph_builder.set_entry_point(STATE_GENERATION)

        memory = MemorySaver()

        self.graph = graph_builder.compile(checkpointer=memory, interrupt_before=[STATE_MEDICAL_APPROVAL, STATE_COMPLIANCE_APPROVAL, STATE_BRAND_APPROVAL, STATE_SEND_COMMUNICATION])

        # with open("drug_workflow.png", "wb") as file:
        #     png_data = self.graph.get_graph().draw_mermaid_png()
        #     file.write(png_data)

    def start_workflow(self):
        self.active = True

        inputs = {"messages" : [HumanMessage(content="Hello")]}

        self.thread = {"configurable": {"thread_id": self.drug["name"]}}

        for event in self.graph.stream(inputs, self.thread, stream_mode="values"):
            print(event)

    def resume_workflow(self):
        name = self.drug["name"]
        if not self.active:
            print(f"Workflow no longer active for {name}. Exiting")
            return
        else:
            for event in self.graph.stream(None, self.thread, stream_mode="values"):
                print(event)
        
    def stop_workflow(self):
        name = self.drug["name"]
        print(f"Stopping workflow for {name}. Exiting")
        self.active = False