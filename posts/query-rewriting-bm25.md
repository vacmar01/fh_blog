---
title: "The Best of Both Worlds: Combining Query Rewriting with Keyword-Based Search"
date: 2025-03-13T15:27:52+01:00
draft: false
excerpt: How to use decorators to elegantly define layouts in FastHTML
---

Keyword-based search, like BM25, remains a strong baseline for retrieval in many RAG applications. Especially if you deal with jargon-heavy text, like in medicine, a keyword-based search approach is very powerful. 

Many user queries are formulated as a question, while the correct source often states the facts as a statement.This 'semantic mismatch' between queries and source content often challenges vector-based search systems. Keyword-based algorithms like BM25 don't care since they don't actually capture the semantic meaning but only the keywords in the questions.

But keyword-based search has a major weakness: Typos. 

Since keyword-based search relies on exact matches, it treats "problem" and "porblem" as entirely different words. We as humans can probably guess that the second word is just a typo of the first and search for the correct documents, but for a naive keyword-based search algorithm these are two different searches. 

But, we can actually still leverage the great performance of BM25 while making our system more robust against typos and other problems of our queries: We can use an LLM to rewrite the user query in a consistent, but keyword-friendly format, while correcting typos and other stuff that might trip up our retrieval mechanism.  

Here is how: 

I'm a huge fan of the `claudette` library by the [answer.ai](https://answer.ai) team, which wraps the Anthropic/Claude API in a really nice python package. The [source code](https://claudette.answer.ai/core.html) is also very readable, it's basically a well documented Jupyter Notebook.

It implements a `client.structured()` method that lets you specify a query and a "return type" that will be called with the response of the model. This "return type" can be a function, like a retrieval function that will be called with arguments specified by the LLM. 

It turns out we can use this method to let a LLM rewrite the user query and call our retrieval function with it: 


```
def retrieve_chunks(
        query: str # the search query to retrieve the most relevant parts using BM25 retrieval.
    ) -> str: # Returns the most relevant parts of the database
    "Uses semantic search to retrieve content from your database."

    retriever = BM25Retriever.from_defaults(
        nodes=nodes,
        similarity_top_k=5,
    ) # This uses BM25 retrieval from llama_index, but any keyword-based retriever would work here.
    
    retrieved_nodes = retriever.retrieve(query)

    return retrieved_nodes

import claudette

client = claudette.Client(claudette.models[1]) # this uses Sonnet 3.7
print(client.structured("Wahts the maening of live?", retrieve_chunks))
```

This all it takes. As you can see claudette uses a very elegant way of documenting its tools called "docments", which are basically inline comments behind the function arguments and return values as well as a normal document string inside of the function body. Behind the scenes, claudette generates a full function schema from it, which allows structured responses from the LLM: 
```
{'name': 'retrieve_chunks',
 'description': 'Uses semantic search to retrieve content from your database.\n\nReturns:\n- type: string',
 'input_schema': {'type': 'object',
  'properties': {'query': {'type': 'string',
    'description': 'the search query to retrieve the most relevant parts using BM25 retrieval.'}},
  'title': None,
  'required': ['query']}}
```

The last line of code returns the result of `retrieve_chunks` after calling it with an LLM-generated query.

That's it. That's literally all you need to improve your BM25-based search engine with LLM-based query rewriting. This approach mitigates many of BM25’s shortcomings, making your system more robust while preserving its strong performance 🚀.