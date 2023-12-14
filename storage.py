import os

from llama_index import SimpleDirectoryReader, ServiceContext, VectorStoreIndex, StorageContext, load_index_from_storage


def create_index():
    documents = SimpleDirectoryReader("docs").load_data()
    service_context = ServiceContext.from_defaults(chunk_size=1024)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context, show_progress=True)
    index.storage_context.persist()
    return index


def get_index():
    if not os.path.exists("./storage"):
        index = create_index()
    else:
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)

    return index
