# llama-rag

The purpose of this project is to show, how to use llama-index to:
- load documents
- create vector index from document embeddings
- use RAG, re-ranking and LLM synthesis to query documents

## Tech details
### Loading (ingesting data)
- The pdf document `Consolidation of Defined Benefit Pension Schemes` is mostly text, but contains a few pages with images and tables. Pdf readers can't handle those very well (if at all). The more images you have, the lower the result accuracy, since you're basically missing data in the loading process. I resolved this by taking screenshots of the pages containing images, and used Chat-GPT to create summaries of the image contents. (Other option would be to automatically send the pages containing images to OpenAI's Vision API, but since there were only 5 pages, I did this manually.). Since I already had summaries of the pages with images, I removed those from the original document.

### Indexing
- I created a vector index from both documents, the original one with image pages removed and the document containing summaries. Llama-index uses `text-embedding-ada-002` by default. This is good and cost-effective model for creating embeddings.
- Setting the chunk size is an important step, since it affects the accuracy. The optimal size varies by document. You can try different chunk settings and use for example [ragas]("https://github.com/explodinggradients/ragas") to assess the accuracy. This can, however, be quite expensive. I chose chunk size of `1024`, since it seems to give good results in general.

### Storing
- The vector index is stored to local disk under `storage`, and it is loaded from there when the app starts.
- In addition, the prompts and responses are saved to disk under the `results` folder.

### Querying
Querying happens as follows:
- User inputs the question as a prompt
- Load the top-k similar nodes (where k=10). Similarity search returns nodes that are *similar* to the query, but they are not necessarily *relevant*. Accuracy can be enhanced by re-ranking the nodes from similarity search so that the most relevant ones get high ranking, and using only the most relevant nodes. It's good to initially have a large amount of nodes, this way there's higher chance that relevant information is included, and re-ranker has enough nodes to work on. 
- Use LLM re-ranker (gpt-4) to determine and return the most relevant ones (top-3).
- use LLM (gpt-4) to answer the question, the input being the question and the most relevant nodes

## Set-up
- **!!! IMPORTANT !!!** You need to add a `.env`-file to the same level where the `main.py`-file is. Add your OpenAI API key there like so:
  ```
  OPENAI_API_KEY="<YOUR_OPEN_AI_API_KEY_HERE>"
  ```
- run the `setup.bat` to set up the virtual environment and install packages
 
## Running
- To run the app, add your question as a command-line parameter inside quotation marks, for example:
- `python main.py "What is a Superfund"`
- If you want to see the debug logs, add a `--debug` flag, for example: `python main.py "What is a Superfund" --debug`
- You'll see the results in console, and your prompt and response are stored into `storage`-folder.

## Notes
- So far, I don't know how to see how many tokens were consumed. They should be exposed in response, but I don't see them.
- Trying to decompose complex queries like "How does the government's response on proposal ABC take into account condition XYZ" to a batch of smaller queries doesn't work out of the box (following example), probably requires building custom retrieval


Links:

Document loading:
- https://blog.langchain.dev/multi-modal-rag-template/ --> how to load documents with lots of images

Retrieval granularity:
- https://arxiv.org/abs/2312.06648 --> introduces a concept of storing data as propositions, looks promising, but lots of manual set-up, consumes lots of tokens

Chunking
- https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
- to determine the optimal, you can try different chunking options and validate with ragas -> expensive!

Re-ranking:
- There's different re-rankers, for example https://txt.cohere.com/rerank/ (commercial, paid)



