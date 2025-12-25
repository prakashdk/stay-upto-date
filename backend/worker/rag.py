import click
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool

embeddings=OllamaEmbeddings(model='embeddinggemma')
vector_store=InMemoryVectorStore(embeddings)


class Ingest:
    def __init__(self):
        print('Initializing Ingestor...')

    def load_data(self):
        import bs4
        from langchain_community.document_loaders import WebBaseLoader

        print('Loading data from web...')

        bs4_strainer=bs4.SoupStrainer(class_=('post-title', 'post-header', 'post-content'))
        loader=WebBaseLoader(web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",), bs_kwargs={'parse_only': bs4_strainer})
        self.docs=loader.load()

        return self
    def split_data(self):
        from langchain_text_splitters import RecursiveCharacterTextSplitter

        print('Data split into chunks...')

        text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        self.all_splits=text_splitter.split_documents(self.docs)


        return self
    
    def store(self):
        print('Storing data in vector store...')

        vector_store.add_documents(documents=self.all_splits)

        return self
    
    def ingest(self):
        self.load_data().split_data().store()

        print('Ingestion complete.')


@tool(response_format='content_and_artifact')
def retrieve_context(query: str):
    """Retrieve information to help answer the question."""
    retrieved_docs=vector_store.similarity_search(query, k=2)

    serialized="\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}") for doc in retrieved_docs
    )

    return serialized, retrieved_docs

class RagAgent:
    def __init__(self):
        from langchain_ollama import ChatOllama

        self.model=ChatOllama(model='llama3.2')

        from langchain.agents import create_agent

        tools=[retrieve_context]
        system_prompt=(
            "You have access to a tool that retrieves context from blog post",
            "Use that tool to answer user queries"
        )

        print('Initializing RAG Agent...')

        self.agent=create_agent(self.model,tools=tools, system_prompt=system_prompt)

   
    def ask(self):
        while(True):
            query=input("Enter your query (or 'exit' to quit): ")
            if query.lower()=='exit':
                break

            messages=(
                f"{query}\n\n",
                "Once you get the answer, lookup common extensions of that method"
            )

            for event in self.agent.stream({'messages':[{'role':'user', 'content':messages}]}, stream_mode='values'):
                event['messages'][-1].pretty_print()


@click.command()
@click.option("--ingest", is_flag=True, help="Run the ingest workflow")
@click.option("--run", is_flag=True, help="Run the main workflow")
def main(ingest, run):
    # Ensure only one flag is used
    if ingest and run:
        raise click.UsageError("You can only use one of --ingest or --run")

    if ingest:
        Ingest().ingest()
    elif run:
        RagAgent().ask()
    else:
        raise click.UsageError("You must provide either --ingest or --run")

if __name__ == "__main__":
    main()
