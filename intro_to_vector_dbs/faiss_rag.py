from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain import hub
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters.character import CharacterTextSplitter
from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from dotenv import load_dotenv
from langchain.chains.retrieval import create_retrieval_chain

if __name__ == "__main__":
    load_dotenv()
    text = TextLoader(file_path="rough_work/data/mediumArticle.txt").load()
    text_splitter = CharacterTextSplitter(chunk_size = 1000, chunk_overlap = 30)
    documents = text_splitter.split_documents(text)
    embedding = OpenAIEmbeddings(model = "text-embedding-3-small")
    vector_store = FAISS.from_documents(documents, embedding)
    llm = ChatOpenAI(model = "gpt-4o-mini", temperature = 0)
    retrieval_prompt = hub.pull("langchain-ai/retrieval-qa-chat")
    retrieval_stuff_chain = create_stuff_documents_chain(llm = llm, prompt = retrieval_prompt)
    retrieval_chain = create_retrieval_chain(retriever=vector_store.as_retriever(), combine_docs_chain = retrieval_stuff_chain)
    sample_result = retrieval_chain.invoke({"input": "What is a vectordb"})
    print(sample_result)