---
title: "Why DSPy is worth using (beyond prompt optimization)"
date: 2025-08-30T15:27:52+01:00
draft: false
excerpt: Let's look at what DSPy offers for AI engineers besides prompt optimization...
image: why_dspy.webp
---

![Why use DSPy](/images/why_dspy.webp)

So if you work with LLMs and logged into X sometime in the last couple of months, I'm sure you've heard about DSPy.

DSPy is a library from Stanford with the slogan: *"Programming — not prompting — LMs"*.

While this slogan is accurate, many people still associate DSPy primarily with automatic prompt optimization. And while this is certainly a very nice feature of DSPy, in my opinion it is not the main selling point of the library.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">why dspy usually wastes your time (and when it doesn&#39;t)<br><br>the question: &quot;should i use dspy for prompt optimization? it seems like the perfect tool for improving my rag system.&quot;<br><br>the answer: dspy is great for very specific, well-defined tasks. but for most rag systems, it&#39;s a…</p>&mdash; jason liu (@jxnlco) <a href="https://twitter.com/jxnlco/status/1960749507399884961?ref_src=twsrc%5Etfw">August 27, 2025</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Apparently an opinionated software library can be very dividing. Some people absolutely hate the idea of DSPy and many people (myself included) absolutely love it.

In this post, I want to dig into what I like most about DSPy, why I think it is a great way of building with LLMs and why people connecting DSPy only with automatic prompt optimization miss out on what makes DSPy so special in my opinion.

So if you looked at DSPy but didn't really understand what the whole hype is all about and if you thought "meh, prompt optimization is not what I want right now", then this one is for you.

## Signatures

DSPy comes with a bunch of new concepts and abstractions for working with LLMs. The most fundamental one of them to understand is called `Signature`. 

"Signatures" are how you tell the LLM what you want and they come in two forms: 

```python
import dspy

llm = dspy.LM("gemini/gemini-2.5-flash-lite")

dspy.configure(lm=llm)

sig1 = "question -> answer"

class Sig2(dspy.Signature): 
    question: str = dspy.InputField()
    answer: str = dspy.OutputField()
```

Signatures are either just a string, describing the input and the desired output separated by an arrow or they can be a subclass of `dspy.Signature`. 

The class approach gives you a little bit more flexibility in describing what exactly you want. You can add task instructions in the class docstring. 

While this may seem odd at first, it's best to think of these instructions as documentation on your task for DSPy, not the LLM directly. There is no guarantee from DSPy that this instruction docstring will get passed to the LLM unchanged. 

Signatures can also be annotated with types, like this `"invoice: str -> total_amount: float"`. DSPy will make sure that the LLM response will be in this format by automatically parsing whatever the LLM returns. This is somewhat similar to libraries like `instructor` or `outlines`, although technically different under the hood.

But how do we now actually use these "Signatures"? 

This is where the second important concept from DSPy comes into play: "Modules"

## What are Modules?

Now that we know what Signatures are, we need to talk about the second important concept: "Modules". 

Modules wrap your Signature and determine how the LLM should try and satisfy the intent you specified in your Signature. 

This may be a little bit abstract, so let's go with an example. 

```python
qa = dspy.Predict(sig1)

qa(question="What is the capital of france?")
```

```
Prediction(
    answer='The capital of France is Paris.'
)
```

As you can see, we wrapped our simple text-based signature in a `dspy.Predict()` module. 

This module is the simplest one. It will create a text prompt from the Signature (using Adapters, but that's a topic for another time), send it to the LLM and parse the output into a `Prediction` class with the output field as an attribute. 

The power of this may be more obvious with another example: 

```python
mult_sig = "number_a: int, number_b: int -> sum: int"

mult = dspy.Predict(mult_sig)

mult(number_a = 5, number_b = 13)
```

```
Prediction(
    sum=18
)
```

Note two things: 

1. DSPy parsed the output as an int and put it in the defined output field automatically. No need to parse xml or json yourself. It also supports complicated Pydantic models without any additional work. 

2. The LLM knew that you wanted to calculate the `sum` from the two numbers, just from the Signature. No need for additional instructions or anything. The input and output field names convey semantic meaning and are thus one of the "knobs" you can use to alter the LLMs performance. 

But what if we have a harder math problem for the LLM and want to give it some tokens for thought? No problem, that's just one line of code change. 

```python
mult_cot = dspy.ChainOfThought(mult_sig)

mult_cot(number_a = 5, number_b = 13)
```

```
Prediction(
    reasoning='The user wants to sum two numbers, 5 and 13. The sum is 18.',
    sum=18
)
```

That's it. That's how you activate chain of thought prompting. 

What if you wanted to solve this problem with an agent that can actually calculate stuff so you don't have to rely on the wonky math abilities of LLMs. 

No problem, again, minimal code change. 

```python
def calculate_sum(a: int, b: int) -> int:
    """calculate the sum of two numbers"""
    return a+b

mult_agent = dspy.ReAct(mult_sig, tools=[calculate_sum])

mult_agent(number_a=5, number_b=13)
```

```
Prediction(
    trajectory={'thought_0': 'The user has provided two numbers, 5 and 13. The goal is to calculate their sum. The `calculate_sum` tool can be used for this purpose. I will call `calculate_sum` with `a=5` and `b=13`.', 'tool_name_0': 'calculate_sum', 'tool_args_0': {'a': 5, 'b': 13}, 'observation_0': 18, 'thought_1': 'The sum of 5 and 13 is 18. I have successfully calculated the sum. I can now use the `finish` tool to signal that the task is complete.', 'tool_name_1': 'finish', 'tool_args_1': {}, 'observation_1': 'Completed.'},
    reasoning='The user wants to find the sum of two numbers, 5 and 13. I used the `calculate_sum` tool with `a=5` and `b=13`, which returned 18.',
    sum=18
)
```

```python
mult_agent(number_a=123122, number_b=3122312)
```

```
Prediction(
    trajectory={'thought_0': 'The user has provided two numbers, number_a and number_b. I need to calculate their sum. The `calculate_sum` tool can be used for this purpose. I will call this tool with the provided numbers.', 'tool_name_0': 'calculate_sum', 'tool_args_0': {'a': 123122, 'b': 3122312}, 'observation_0': 3245434, 'thought_1': 'The sum has been calculated. I can now finish the task.', 'tool_name_1': 'finish', 'tool_args_1': {}, 'observation_1': 'Completed.'},
    reasoning='The user asked to calculate the sum of two numbers. I used the `calculate_sum` tool to add `number_a` (123122) and `number_b` (3122312). The result of the sum is 3245434.',
    sum=3245434
)
```

Boom, you just created an AI agent that can calculate the sum of two numbers (did I hear "overengineered"?).

As you can see, through "Modules" and "Signatures" DSPy seperates the task definition or specification (Signature) from the Inference strategy to achieve this Task (Module). 

That's Engineering 101. Why should the task specification be connected to the inference strategy and to the format we want to receive the answer in? That makes no sense. But normal free text prompts force you to specify everything in one long and filthy string of text, that's hard to reason about after a certain scale and which is hard to iterate on fast enough (*evals evals evals*).

In my opinion that alone makes using DSPy worth it. 

And it also makes task decomposition easier. 

Let's say you want to summarize a huge regulatory document. 

Sure you could specify a Signature like "document -> summary" and with modern long-context LLMs you may even fit the whole 1000 page document into the context as markdown into the context window. 

But maybe you are not satisfied with the result. The summary is sloppy and not very helpful. 

So you think: "Maybe it's better to decompose the summary task into multiple tasks. I'll split the document into chapters and let the LLM summarize each chapter and then I'll combine these chapter summaries into one document summary". 

DSPy got your back here. 

That's where custom "Modules" come into play (honestly, this may be a bit confusing in terms of terminology). 

Think of these custom Modules as a PyTorch Module. But instead of specifying neural layers (like `nn.Linear`), you specify submodules (like `dspy.Predict("chapter -> summary")`) and combine these calls together. A custom module for a task decomposition I described above would look like this:  

```python
class DocumentSummarizer(dspy.Module):
    def __init__(self):
        self.summarize_chapter = dspy.ChainOfThought("chapter -> summary")
        self.create_document_summary = dspy.ChainOfThought("chapter_summaries: list[str] -> document_summary")

    def forward(self, document: str): 
        chapters = document.split("##")
        chapter_summaries = []
        for chapter in chapters: # can be parallelized ofc
            chapter_summary = self.summarize_chapter(chapter=chapter).summary
            chapter_summaries.append(chapter_summary)
        
        document_summary = self.create_document_summary(chapter_summaries=chapter_summaries).document_summary

        return dspy.Prediction(summary=document_summary)
```

As you can see, this looks a lot like a PyTorch module. But from the outside it behaves exactly the same as a simple `dspy.Predict("document -> summary")` module. What happens inside is none of your business as the user, as long as it delivers on its task. 

And again, this is the power of abstractions and modularity. DSPy's Modules encapsulate and abstract away inference time strategies beautifully.  

## A word on developer ergonomics

Did you see how little code we wrote? We didn't write long lists with lots of `{"role": "user", "content": "..."}` objects. We also didn't need to extract the actual response from the response object with such atrocious code as `res.choices[0].message.content` (is content an attribute or key of `message`? I forgot) just to put this string through another function which extracts the actual content from xml tags.

That's just so much boilerplate and ceremony that is all abstracted away for you so you can concentrate on what you actually want to achieve, fast. 

## Conclusion

As you can see, I didn't speak about prompt optimizers. Not because I don't think they are extremely cool, but because I think they are not at the heart of DSPy. They are downstream of the abstractions DSPy provides. Through the abstractions DSPy has a deep insight into what you actually want to achieve and can help you do that. Much like a compiler parses your code and then optimizes it however it wishes, as long as it still does what you intended to do. If you know PyTorch it is maybe good to think of Prompt Optimizers like `torch.compile`. I personally never had to use it in PyTorch.

And similarly, DSPy brings so much value to you as an AI engineer even if you don't use prompt optimizers. 

And it helps you iterate fast on your AI program with better "knobs" than changing random words in a long piece of text. 

===================================================

Wanna talk AI Engineering? Hit me up on [Twitter](https://twitter.com/rasmus1610)
