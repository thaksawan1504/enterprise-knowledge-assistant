import os
import httpx

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


class RAGBrain:

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_API_BASE")
        model_name = os.getenv(
            "OPENAI_MODEL_NAME",
            "gpt-5-chat"
        )

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY missing in .env"
            )

        custom_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        custom_client = httpx.Client(
            verify=False,
            headers=custom_headers
        )

        self.retriever = None
        self.chain = None

        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.1,
            openai_api_key=api_key,
            openai_api_base=base_url,
            http_client=custom_client,
            max_retries=0
        )

    def process_document(self, pdf_path):

        if not os.path.exists(pdf_path):
            raise FileNotFoundError(
                f"PDF not found: {pdf_path}"
            )

        print("STEP 1 : Loading PDF")

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        print("STEP 2 : Splitting Chunks")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(docs)

        print(
            f"STEP 3 : Total Chunks = {len(chunks)}"
        )

        print(
            "STEP 4 : Creating HuggingFace Embeddings"
        )

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        print(
            "STEP 5 : Building FAISS Vector Store"
        )

        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )

        print(
            "STEP 6 : Creating Retriever"
        )

        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )

        self._build_chain()

        return len(chunks)

    def _build_chain(self):

        prompt = ChatPromptTemplate.from_template(
            """
You are a professional AI assistant.

Answer only from the provided context.

If the answer is not present in the context,
reply with:

I cannot find the answer in the document.

Context:
{context}

Question:
{question}
"""
        )

        def format_docs(docs):
            return "\n\n".join(
                doc.page_content
                for doc in docs
            )

        self.chain = (
            {
                "context": self.retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def execute_query(self, query):

        if not self.chain:
            return "Document not processed."

        try:
            response = self.chain.invoke(query)
            return response

        except Exception as e:
            return f"Query Failed: {str(e)}"