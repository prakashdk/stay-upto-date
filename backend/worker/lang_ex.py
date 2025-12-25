from langchain_community.document_loaders import PyPDFLoader
from pprint import pprint

file_path='./data/nke-10k-2023.pdf'

loader=PyPDFLoader(file_path)

docs=loader.load()

# print(len(docs))
# pprint(docs[0].metadata, indent=4)
# print(docs[0].page_content[:200])


from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)

all_splits=text_splitter.split_documents(docs)

# print(len(all_splits))

from langchain_ollama import OllamaEmbeddings

embedding_model=OllamaEmbeddings(model='embeddinggemma')

vector1=embedding_model.embed_documents(all_splits[0].page_content)
vector2=embedding_model.embed_documents(all_splits[1].page_content)

# print(len(vector1)==len(vector1[0]))

from langchain_core.vectorstores import InMemoryVectorStore

vector_store=InMemoryVectorStore(embedding_model)

ids=vector_store.add_documents(documents=all_splits)

# print(ids)

results=vector_store.similarity_search_with_score(query='How many distribution centers does Nike have in the US?', k=1)

pprint(results, indent=4)