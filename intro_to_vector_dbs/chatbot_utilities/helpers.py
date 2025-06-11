from langchain_pinecone import PineconeVectorStore
from langchain_community.document_loaders.readthedocs import ReadTheDocsLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.chains.history_aware_retriever import create_history_aware_retriever

from dotenv import load_dotenv


def ingest_docs(filePath, index_name, embedding_model):
    """
    To use this functions
    file_path = "../data/langchain-docs/api.python.langchain.com/en/latest/"
    ingest_docs(filePath = file_path, index_name = some_name, embedding_model =some_model)
    """
    loader = ReadTheDocsLoader(filePath)
    text = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = splitter.split_documents(text)
    embeddings = OpenAIEmbeddings(model=embedding_model)
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)

    batch_size, ingestion_id_all = 256, []
    for index in range(0, len(documents), batch_size):
        try:
            batch_insert_entitiy = documents[index : index + batch_size]
        except Exception as e:
            batch_insert_entitiy = documents[index:]

        ingestion_ids = vector_store.add_documents(batch_insert_entitiy)
        ingestion_id_all.extend(ingestion_ids)
        print(".", end="")


def get_rag_agent(model, index_name, embeddings, chat_history=[]):
    """
    retrieval_qa_agent = get_rag_agent(model = "gpt-4o-mini", index_name = "langchain-chabot", embeddings = "text-embedding-3-small")
    """
    retrieval_qa = hub.pull("langchain-ai/retrieval-qa-chat")
    llm = ChatOpenAI(model=model, streaming=True)
    embeddings = OpenAIEmbeddings(model=embeddings)
    vector_store = PineconeVectorStore(index_name=index_name, embedding=embeddings)
    combine_docs_chain = create_stuff_documents_chain(llm=llm, prompt=retrieval_qa)

    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    history_aware = create_history_aware_retriever(
        llm=llm, retriever=vector_store.as_retriever(), prompt=rephrase_prompt
    )

    retrieval_qa_agent = create_retrieval_chain(
        retriever=history_aware, combine_docs_chain=combine_docs_chain
    )

    return retrieval_qa_agent


if __name__ == "__main__":
    load_dotenv()
    retrieval_qa_agent = get_rag_agent(
        model="gpt-4o-mini",
        index_name="langchain-chabot",
        embeddings="text-embedding-3-small",
    )
    answer = retrieval_qa_agent.invoke(
        {"input": "How to use configure json parser in langchain"}
    )["answer"]
    print("\n\n*********")
    print(answer)
    print("\n\n*********")
