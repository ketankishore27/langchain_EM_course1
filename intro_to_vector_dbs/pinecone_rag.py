import os
from dotenv import load_dotenv
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain import hub
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain


def make_ingestion(vector_Store):
    loader = TextLoader(r"rough_work/data/mediumArticle.txt")
    text = loader.load()

    splitter = CharacterTextSplitter(
        separator="\n\n", chunk_size=1000, chunk_overlap=100
    )

    text_splits = splitter.split_documents(text)
    print("Ingestion")
    vector_Store.add_documents(text_splits)
    print("Ingestion Finish")


if __name__ == "__main__":

    load_dotenv()
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = PineconeVectorStore(
        index_name="medium-blogs-embedding-index", embedding=embeddings
    )

    make_ingestion_flag = False
    if make_ingestion_flag:
        make_ingestion(vector_store)

    print("Retrieval paradigm")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    rag_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    retrieval_qa_chain = create_stuff_documents_chain(llm, rag_prompt)
    retrieval_chain = create_retrieval_chain(
        retriever=vector_store.as_retriever(), combine_docs_chain=retrieval_qa_chain
    )

    sample_Result = retrieval_chain.invoke({"input": "How can i use a vector DB"})
    print(sample_Result["answer"])
