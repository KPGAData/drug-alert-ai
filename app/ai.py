import os
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_core.output_parsers.string import StrOutputParser
from langchain.output_parsers.combining import CombiningOutputParser
import posixpath
from langgraph.prebuilt import ToolExecutor
from pathlib import Path
from dotenv import load_dotenv
import datetime
import dateutil.parser

class AI:
    def __init__(self) -> None:
        self.model = None
        self.tool_belt = []
        self.tool_executor = None

        self.source_pdf_dir = None
        self.retreiver = None
        self.rag_prompt = None

    def load_model(self) -> None:
        self.model = ChatOpenAI(model="gpt-4o", temperature=0)

    def load_embeddings(self) -> None:
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    def load_tools(self) -> None:
        self.tool_belt = [
            DuckDuckGoSearchRun(),
            ArxivQueryRun()
        ]

        self.tool_executor = ToolExecutor(self.tool_belt)
        functions = [convert_to_openai_function(t) for t in self.tool_belt]
        self.model = self.model.bind_functions(functions)
    

    def loadDrugData(self, arg) -> None:
        #1. Set path for drug pdf document & load OpenAI API Key & embedding model
        PROJECT_DIR = Path(__file__).parent.parent
        self.project_dir = PROJECT_DIR

        SOURCE_PDF_DIR = PROJECT_DIR / 'data' / 'PI'
        joined_path = os.path.join(SOURCE_PDF_DIR , arg.drug["name"] + '.pdf')
        self.source_pdf_dir = joined_path
        print(self.source_pdf_dir)

        load_dotenv()
        OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
            
    def retrieveAndCreateEmbeddingStore(self) -> None:
        #2. Load PDF Document
        loader = PyMuPDFLoader(self.source_pdf_dir)
        documents = loader.load()
        print(len(documents))

        #3. Perform chunking
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size = 200,
            chunk_overlap = 25
        )
        documents = text_splitter.split_documents(documents)

        #4 Store embeddings in QDrant vector store in memory
        from langchain_community.vectorstores import Qdrant
        qdrant_vector_store = Qdrant.from_documents(
            documents,
            self.embeddings,
            location=":memory:",
            collection_name="Drug prescription and general information",
        )
        qdrant_retriever = qdrant_vector_store.as_retriever()
        self.retreiver = qdrant_retriever

    def createPrompt(self, arg) -> None:
        #5 Query for search
        query = "Provide highlights for the Drug" + arg.drug["name"]

        #6 Setting up RAG Prompt Template
        from langchain_core.prompts import PromptTemplate

        RAG_PROMPT_TEMPLATE = os.getenv("RAG_PROMPT_TEMPLATE")
        RAG_PROMPT_TEMPLATE = RAG_PROMPT_TEMPLATE.replace("drug_name", arg.drug["name"])

        # print("RAG_PROMPT_TEMPLATE")
        # print(RAG_PROMPT_TEMPLATE)

        rag_prompt = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)
        self.rag_prompt = rag_prompt

    def generateTempleteFromAI(self, arg) -> None:
        
        #8 Create LLM endpoint
        from operator import itemgetter
        from langchain.schema.output_parser import StrOutputParser
        from langchain.schema.runnable import RunnablePassthrough

        lcel_rag_chain = (
                {"context": itemgetter("query") | self.retreiver, 
                "query": itemgetter("query"), 
                }
                
                | self.rag_prompt | self.model
            )

        filename  =  self.project_dir / 'data' / 'output' / 'generated' /  arg.drug["name"] 
        filename  =  f"{filename}.txt"
        GENERATED_FILE = os.path.dirname(filename)
        str_parser = StrOutputParser()

        str_parser = lcel_rag_chain.invoke({"query": arg.drug["name"]})

        f = open(filename, "w")   # 'r' for reading and 'w' for writing
        f.write(str_parser.content )    # Write inside file 
        f.close()    