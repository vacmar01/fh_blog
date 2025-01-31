---
title: How to Use Modal to run ColBERTv2
date: 2024-12-31T11:20:06+01:00
draft: false
excerpt: How to use Modal.com to run ColBERTv2 through the ragatouille library
---

Recently, I stumbled across [Modal](https://modal.com).

Modal is a "serverless compute platform". What does that even mean?

Actually, the idea behind Modal is quite genius.

It let's you seemlessly run python code in the cloud, use GPUs for specific parts of your code and even scale code horizontally on multiple containers with a single line of code.

It's especially handy for data-heavy tasks like scraping a lot of URLs in parallel, munching huge DataFrames or training neural networks.

Also recently, I stumbled across so called "late interaction models" for information retrieval, like "ColBERT". They are the new hot shit (apparently) because they improve some of the weaknesses of typical dense vector embeddings, often used for vector-based semantic search.

Fortunately the ["ragatouille"](https://github.com/AnswerDotAI/RAGatouille/) python package by [Benjamin Clavie](https://x.com/bclavie) makes it super simple to work with these kinds of models.

But they need a lot of RAM/VRAM to create to index documents and also the retrieval part is much faster if you do it on a GPU.

This sounds to like it is a perfect little excuse to try out [Modal](https://modal.com).

This is all the code it takes:

```python
#filename: colbert_index.py

import modal
from ragatouille import RAGPretrainedModel
from llama_index.core import SimpleDirectoryReader

app = modal.App("colbert-index")

MODEL = "colbert-ir/colbertv2.0"

def load_model():
    from ragatouille import RAGPretrainedModel
    rag = RAGPretrainedModel.from_pretrained(MODEL)

cuda_version = "12.4.0"  # should be no greater than host CUDA version
flavor = "devel"  #  includes full CUDA toolkit
operating_sys = "ubuntu22.04"
tag = f"{cuda_version}-{flavor}-{operating_sys}"

rag_image = (modal.Image.from_registry(f"nvidia/cuda:{tag}", add_python="3.11")
             .pip_install("llama-index", "ragatouille")
             .apt_install("git")
             .run_function(load_model)
)

volume = modal.volume.Volume.from_name("ragatouille-indexes", create_if_missing=True)

@app.function(gpu="A100", image=rag_image, timeout=600, volumes={"/index": volume})
def create_index(docs):
    docs_text = [doc.text for doc in docs]
    docs_metadata = [doc.metadata for doc in docs]

    rag = RAGPretrainedModel.from_pretrained(MODEL, index_root="/index")

    rag.index(
        collection=docs_text,
        index_name="leitlinien",
        max_document_length=512,
        split_documents=True,
        document_metadatas=docs_metadata
        # use_faiss=True, # use only when you can sure that faiss is working on your system
    )

@app.local_entrypoint()
def main():
    docs = SimpleDirectoryReader(input_dir="./pdfs").load_data()
    create_index.remote(docs)

```

Okay, let's break it down.

First things first. Let's install `modal`, `llama-index` and `ragatouille` using pip: `pip install ragatouille modal`. We'll use `llama_index` to read in our PDFs.

```python
import modal
from ragatouille import RAGPretrainedModel
from llama_index.core import SimpleDirectoryReader

app = modal.App("colbert-index")

MODEL = "colbert-ir/colbertv2.0"

def load_model():
    from ragatouille import RAGPretrainedModel
    rag = RAGPretrainedModel.from_pretrained(MODEL)

cuda_version = "12.4.0"  # should be no greater than host CUDA version
flavor = "devel"  #  includes full CUDA toolkit
operating_sys = "ubuntu22.04"
tag = f"{cuda_version}-{flavor}-{operating_sys}"

rag_image = (modal.Image.from_registry(f"nvidia/cuda:{tag}", add_python="3.11")
             .pip_install("llama-index", "ragatouille")
             .apt_install("git")
             .run_function(load_model)
)
```

First we import everything we need from the `ragatouille` module. We'll use llama_index to read in the pdfs from a folder.

Then we define a function called `load_model()`that loads the model weights from [HuggingFace](https://huggingface.co), more on this later.

Modal functions run in containers in the cloud. If we need anything except the python standard library, we have to install it in the container.

Since we want to make sure that out ColBERT indexing runs on a GPU, we have to make sure that we have a container image with all the CUDA stuff installed. I run in some problems with the normal `debian_slim()` image, so I picked another CUDA image from the docker hub. Then we'll install `llama-index` and `ragatouille` in the container through `pip` and of course `git` to fetch the model weights from HF.

Look how nice the developer experience is with the `pip_install` and `apt_install` functions.

Then we run our previously defined `load_model()` function, to prefetch the model weights. All of these "build steps" are cached, this means the model weights will be cached too and can be retrieved faster later when we need them on a subsequent run.

```python
volume = modal.volume.Volume.from_name("ragatouille-indexes", create_if_missing=True)
```

Next, we'll define a volume. A volume is a persistent storage between creations of the containers. the filesystem of the container will be destroyed after every run. So if you want to store something permanently, retrieve it from the Modal cloud or share stuff between containers (or Modal functions), you have to create a `volume`.

Now we come to the heart of the whole script.

```python
@app.function(gpu="A100", image=rag_image, timeout=600, volumes={"/index": volume})
def create_index(docs):
    docs_text = [doc.text for doc in docs]
    docs_metadata = [doc.metadata for doc in docs]

    rag = RAGPretrainedModel.from_pretrained(MODEL, index_root="/index")

    rag.index(
        collection=docs_text,
        index_name="leitlinien",
        max_document_length=512,
        split_documents=True,
        document_metadatas=docs_metadata
        # use_faiss=True, # use only when you can sure that faiss is working on your system
    )
```

We define our function `create_index` that does all of the actual work.

Modal works with decorators a lot. `the @app.function` decorator turn the python function into a Modal function. Here we can also specifiy that we would like to have a GPU for this, what image to use and where to mount our volume.

I had problems with "CUDA Out of Memory" errors on smaller GPUs than a A100. I have to dig into, what's the problem here.

The function is pretty easy and mostly copied from the `ragatouille` documentation. We load the pretrained model (again) and specify where the index should be saved to. This is the directory we mounted our volume into. Then we call `rag.index()` with our documents and specify the max_document_length the documents will be split into.

Now we just need a way to run this function on Modal.com.

```python

@app.local_entrypoint()
def main():
    docs = SimpleDirectoryReader(input_dir="./pdfs").load_data()
    create_index.remote(docs)

```

The `@app.local_entrypoint()` decorator specifies what function to run when we run this script on Modal.com.

The `main()` function does nothing else than reading in our pdfs from the folder. Then it calls the `create_index` function and passes in the read-in docs as arguments. Note the `.remote()` call here. This tells modal that we want to run the `create_index()` function remotely on Modal's infrastructure. We could also call `create_index.local(docs)` to run the same function locally on our local machine.

There is also a handy `.map()`, which let's you run a function on multiple inputs in parallel, but this doesn't really make sense here for us, but is handy to have.

I'm really amazed by how easy it is to run certain code on GPUs using Modal.com. And you only pay for the time the GPU actually runs, which means that it is really cost-effective. Indexing two PDFs with 400 pages in total costs around 10 cents for me.

Next up I want to learn how to actually retrieve documents from our newly created index given a certain query using Modal.

Thank you to Jay Shah, the following blog post helped me alot: https://jayshah5696.github.io/ragatouillie/
