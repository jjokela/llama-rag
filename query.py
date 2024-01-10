import logging
import os
import sys

from llama_index import get_response_synthesizer, ServiceContext
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.llms import OpenAI, AzureOpenAI
from llama_index.postprocessor import SimilarityPostprocessor, LLMRerank
from llama_index.query_engine import RetrieverQueryEngine


def set_debug():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_synthetized_results(index, question):
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
    )

    response_synthesizer = get_response_synthesizer()

    query_engine = RetrieverQueryEngine(
        retriever=retriever,
        response_synthesizer=response_synthesizer,
        node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
    )

    return query_engine.query(question)


def get_reranked_results(index, query_str, reranker_top_n=3):
    azure_api_key = os.getenv('AZURE_OPENAI_INSTANCE_KEY')
    api_url = os.getenv('AZURE_OPENAI_LANGUAGE_API_URL')

    # llm = OpenAI(temperature=0, model="gpt-4")

    llm = AzureOpenAI(
        model="gpt-3.5-turbo",
        deployment_name="gpt-3.5-turbo",
        api_key=azure_api_key,
        azure_endpoint=api_url,
        api_version='2023-05-15',
    )

    service_context = ServiceContext.from_defaults(llm=llm, chunk_size=1024)

    reranker = LLMRerank(
        choice_batch_size=5,
        top_n=reranker_top_n,
        service_context=service_context,
    )

    query_engine = index.as_query_engine(
        similarity_top_k=10,
        node_postprocessors=[reranker],
        response_mode="tree_summarize",
    )

    return query_engine.query(query_str)
