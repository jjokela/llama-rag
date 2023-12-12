import os
import logging
import pprint
import sys
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, \
    get_response_synthesizer, QueryBundle, ServiceContext
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.llms import OpenAI
from llama_index.postprocessor import SimilarityPostprocessor, LLMRerank
from llama_index.query_engine import RetrieverQueryEngine

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_index():
    if not os.path.exists("./storage"):
        documents = SimpleDirectoryReader("docs").load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist()
    else:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)

    return index


def get_retriever(index):
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    return retriever


def get_query_engine(index):
    return index.as_query_engine()


def ask(query_engine, question):
    response = query_engine.query(question)
    return response


def get_synth_results(index, question):
    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    # configure response synthesizer
    response_synthesizer = get_response_synthesizer()

    # assemble query engine
    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    return query_engine.query(question)


def get_with_reranker(index, query_str, vector_top_k=10, reranker_top_n=3):
    llm = OpenAI(temperature=0, model="gpt-4-1106-preview")
    service_context = ServiceContext.from_defaults(llm=llm, chunk_size=512)

    query_bundle = QueryBundle(query_str)
    # configure retriever
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=vector_top_k,
    )
    retrieved_nodes = retriever.retrieve(query_bundle)

    # configure reranker
    reranker = LLMRerank(
        choice_batch_size=5,
        top_n=reranker_top_n,
        service_context=service_context,
    )
    # retrieved_nodes = reranker.postprocess_nodes(
    #     retrieved_nodes, query_bundle
    # )

    query_engine = index.as_query_engine(
        similarity_top_k=10,
        node_postprocessors=[reranker],
        response_mode="tree_summarize",
    )
    return query_engine.query(query_str)


if __name__ == "__main__":
    idx = get_index()

    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    else:
        prompt = "What is this document about?"

    res = get_with_reranker(idx, prompt)

    pprint.pprint(res)
