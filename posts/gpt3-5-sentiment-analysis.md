---
title: 'Sentiment Analysis with GPT 3.5'
date: 2024-02-06T20:05:14+01:00
draft: false
---

Did you know that you can classify text into distinct, predefined classes with LLMs like ChatGPT?

Yes it's possible and I'll show you how. 

The big advantage is that these LLMs have a lot of knowledge and text understanding capabilites already encoded in their parameters. This means that their ability to do text classification without any pre-training is really high. 

This is very interesting if you don't have a lot of labeled training data. 

We use the task of sentiment analysis as an example in this notebook. We'll load a dataset with movie reviews and our task is to classify them to be either "positive" or "negative".

First let's import all the libraries we need. We will also use OpenAIs API and their GPT-3.5-turbo model. Additionally we will leverage their function calling capabilities through a library called [instructor](https://github.com/jxnl/instructor). This ensures that the get back only the labels "POSITIVE" or "NEGATIVE" and nothing else. 


```python
import instructor
import openai
from openai import OpenAI
import enum 
from datasets import load_dataset
import numpy as np
from tqdm import tqdm

#load the .env file
from dotenv import load_dotenv
load_dotenv()

#load the API key
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

from pydantic import BaseModel, Field
```

The idea is to use another library called ["pydantic"](https://pydantic.dev/) to specifiy what data we want the LLM to return. We can leverage this to restrict the model output to the classes we want. 

For demonstrating how this works we'll use the ["rotten_tomatoes"](https://huggingface.co/datasets/rotten_tomatoes) dataset from [huggingface.co](https://huggingface.co). This is a dataset of movie reviews from the website ["Rotten Tomatoes"](https://www.rottentomatoes.com/). The movie reviews are either "positive" or "negative" and the task is to classify the movie reviews in one of these two categories. 

Further, we will only use a subset of 100 randomly chosen examples for demonstration purposes here. 

The labels are encoded as integeres with 0 = 'negative' and 1 = 'positive'. With the `itol` dict we map the integers to the actual labels.


```python
dataset = load_dataset("rotten_tomatoes")
subset = dataset["train"].shuffle().select(range(100)) # random subset of 100 examples

# convert the integers to labels
itol = {0: "negative", 1: "positive"}

# an example of the data
subset["text"][2], itol[subset["label"][2]]
```




    ('what [denis] accomplishes in his chilling , unnerving film is a double portrait of two young women whose lives were as claustrophic , suffocating and chilly as the attics to which they were inevitably consigned .',
     'positive')



## The heart of the whole idea
Now we come to the heart of the whole idea.

We leverage data types to describe the data we want to receive back from the model. 

We use an `Enum` to implement our labels `POSITIVE` and `NEGATIVE`. Then we implement a `pydantic` `BaseModel` that describes what the prediction of the LLM should encapsulate. In our very simple case this is just the predicted `class_label`, which is of type `Labels`. 

Note that the docstring here has a function that goes further than just providing documentation. Since the docstring will be part of the schema of the `SinglePrediction` class and the schema will be passed to the LLM, it gives further information to the LLM what this class represents and what the LLM should do. 


```python
class Labels(str, enum.Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    
class SinglePrediction(BaseModel):
    """
    Correct sentiment label for the given text
    """

    class_label: Labels = Field(..., description="the correct sentiment label for the given text")

SinglePrediction.model_json_schema()
```




    {'$defs': {'Labels': {'enum': ['positive', 'negative'],
       'title': 'Labels',
       'type': 'string'}},
     'description': 'Correct sentiment label for the given text',
     'properties': {'class_label': {'allOf': [{'$ref': '#/$defs/Labels'}],
       'description': 'the correct sentiment label for the given text'}},
     'required': ['class_label'],
     'title': 'SinglePrediction',
     'type': 'object'}



The `instructor` library works by "patching" the `openai` client and expanding its functionality. We just call the `instructor.patch()` function with the `OpenAI()` class as its sole argument and use this as our `client`. 


```python
client = instructor.patch(OpenAI())
```

## The `classify` function
Now we can implement the `classify` function that takes in the data we want to classify (our movie reviews) and return an instance of the `SinglePrediction` class we implemented above. 

The code is quite simple and should be familiar to you if you have already used the OpenAI api. It's a normal openai API call with one small difference. Through patching the `OpenAI` class, the `client.chat.completions.create` method has a new parameter called `response_model`. This specifices which `Pydantic` model should be returned by the API call.


```python
def classify(data: str) -> SinglePrediction:
    return client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        temperature=0.4,
        response_model=SinglePrediction,
        messages=[
             {
                "role": "system",
                "content": "You are a world class algorithm to identify the sentiment of movie reviews.",
            },

            {
                "role": "user",
                "content": f"Classify the sentiment of the following movie review: {data}",
            },
        ],
    )
```

Let's define a simple function that calculates the accuracy based on our predictions and the real labels, called `targets` here. We can use it to see how well our no-training sentiment analyis model works.


```python
# calculate accuracy based on preds and targets
def accuracy(preds, targets):
    return np.sum(np.array(preds) == np.array(targets)) / len(preds)
```

Now we have everything to actually predict the sentiment of our movie reviews. Run the code below. It should take around 90 seconds to finish.


```python
preds = [classify(t).class_label.value for t in tqdm(subset["text"])]
targets = [itol[l] for l in subset["label"]]
```

    100%|██████████| 100/100 [01:22<00:00,  1.21it/s]


Now the moment of truth. How well does GPT 3.5 Turbo actually perform. 


```python
accuracy(preds, targets) 
```




    0.95



We get an accuracy of 0.95 ... well, that's much better than random guessing. A specifically trained encoder-only transformer like "Bert" might work better heren, but remember this is without any training whatsoever. That's the power of LLMs for classical NLP tasks. For many tasks using text that is close to the training data, there is no training needed anymore. 

## Conclusion

Think about it how awesome this is: You can build actually helpful stuff with LLMs without the need to gather a lot of training data. Maybe you want to classify customer enquiries into different buckets to route them to different employees or you want to build your own email spam filter. You can build this using ChatGPT et al. out of the box. And libraries like `instructor` make sure that you actually get the output you think you'll get, even with tasks that are very different to what these LLMs have been trained for (classification instead of text generation).  
