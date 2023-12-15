# llama-rag

* high-lvl overview
* * llama-index 
* uses RAG, re-ranking and synthesis
* * user can query stuff

* tech details
* Loading (ingesting data)
  * embeddings (ada)
  * chunk size
  * images summary Chat-GPT, pdf removed images
  * both documents loaded
* Indexing
  * vector index
  * top-k semantic retrieval
* Storing
  * local disk
  * prompts and responses are stored to `asdf`, see some examples
* Querying
  * (see below)
  * gpt-4


* setup
  * run batch

* Notes
  * counting of tokens :(
  * trying to decompose complex queries doesn't work out of the box, probably requires building custom retrieval


models used:
- By default, we use the OpenAI gpt-3.5-turbo model for text generation and text-embedding-ada-002

Loading docs
- the document contains images, and pdf readers can't handle those very well (if at all)
- therefore the more images you have, the lower the accuracy, since you're basically missing data
- getting a summary of the image and adding those embeddings increases the accuracy significantly
- images:
-- for each page that contained image, I took a screenshot and asked Chat-GPT to create summary of it
-- could be automated, but there were only 5 pages
-- if there would be a lot of images (for example slide deck), one option is store both images and summaries, and build an index that links summaries and images, then the response can show the source images as references
- removed the pages that contained images from pdf
- loaded both pdf and summaries, generated embeddings and stored them to a in-memory vector db (index)
- the index is stored into disk, so if it already exists, it is loaded from there



Retrieval methods:
- https://arxiv.org/abs/2312.06648 --> looks promising, but lots of manual set-up, consumes lots of nodes

Chunking
- https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5
- 1024
- to determine the optimal, you can try different chunking options and validate with ragas -> expensive!


Querying and re-ranking
- get top-k similar nodes (k=10)
- use LLM re-ranker (prompt) to determine the most relevant ones
- use LLM to answer the question, the input is the question and most relevant nodes

Similarity search returns nodes that are *similar* to the query, but they are not necessarily *relevant*
Accuracy can be enhanced by re-ranking the nodes from similarity search, and using only the most relevant ones. 
It's good to have initially a large amount of similar nodes, this way there's higher chance that relevant information 
is included, and re-ranker has enough nodes to work on    
There's different re-rankers, for example https://txt.cohere.com/rerank/ (commercial, paid)

