---
title: "Thoughts on Jev"
date: 2026-09-29T21:42:57+02:00
draft: false
excerpt: Jev is the AI moment of 2026 for me. But the interesting part isn't its classifier interface — it's the training objective, and what it means for building with AI.
---

For me, the release of Jev by typesafe.ai is *the* AI moment of 2026 thus far. Here are some of my thoughts on it. 

## A classifier interface with LLM-like generality

What makes Jev interesting is not that it outputs decisions instead of text. The interesting part is that it can make decisions across a wide range of tasks and domains without task-specific training or fine-tuning.

Viewed only through its input and output shape, Jev is indeed nothing new. It's basically what classifiers have done for the past 50 years. Encoder-only transformers like BERT, introduced in 2018, can be used to build classifiers with a very similar input/output shape. And Jev is not even the first zero-shot text classifier either. 

But somehow — at least in my experience — it's the first one that actually works for a *wide* range of tasks. I can make an API call, give it a new question, and get a useful answer without collecting training data or fine-tuning a model. It also handles non-English text well and demonstrates a level of general language understanding that I previously associated mostly with generative LLMs. That combination — not the input/output shape — is what's interesting to me.

## Copying the interface is not enough

Taking a random open-weight model and restraining its output to a closed set of single tokens does not reproduce what makes Jev useful.

The first clones of Jev came out within days of the original model's release. And a lot of people claimed they would have basically built the same in like 2 hours using ChatGPT. One straightforward way to do this is to take an open-weight LLM and constrain it to a single token that encodes the output. So if you have a `Choice` primitive with, let's say, 4 answers, that would mean that the LLM is only allowed to put out A, B, C or D. You just look at the output distribution of the next token after the input, discard everything that doesn't fit your schema, let a softmax function run over the filtered logprobs and voilà, you have an output that looks very similar to what Jev puts out. 

But it misses the point completely. Just because the output looks the same doesn't mean it has the same usefulness.

Many chat LLMs are trained with RLHF — “reinforcement learning from human feedback” — or related preference-optimization methods. Diogo Almeida, the CEO of typesafe.ai, co-authored the [InstructGPT paper](https://arxiv.org/abs/2203.02155) while working at OpenAI. RLHF was a key ingredient of the secret sauce behind the original ChatGPT, which was built on GPT-3.5.

And for chat applications, it works fine. But optimizing for answers humans prefer is not the same as optimizing for reliable decisions. It comes with trade-offs like mode dropping and what I call "confident bullshitting" (If you wanna know more just listen to one of Diogo's recent talks, like [the one here](https://www.youtube.com/watch?v=o-y1HJ6buGQ)). 

And now, if you take an RLHF-trained model and simply restrict its output, you haven't changed what it was trained to do. You've changed the interface, not the objective.

In my opinion, people over-index too much on the model architecture and the input/output shape of Jev and not enough on what is its true moat: the training data and the training objective. 

In my own tests, Jev outperforms all the clones I have tested so far by a lot. Jev seems to be much less jagged and much more generalizable, something that probably comes from the training data and the novel training objective. 

This fits with a point Diogo Almeida makes in [a blog post](https://typesafe.ai/blog/bitterest-lesson) riffing on Rich Sutton’s [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html): compute matters, but so do data and — perhaps most importantly — training on the right task. Jev seems like a culmination of that philosophy. 

Many clones reproduce its interface, but not the task it was trained to perform.

## The model is a black box. The system doesn’t have to be

Simon Willison raises a valid concern about Jev in [his blog post about the model release](https://simonwillison.net/2026/Sep/21/jev/): 

> Jev doesn’t even give you that: put in all the text you want, the only thing you’re going to get back is a floating point number. If Jev marks something as spam, which content signals tipped it off?
> This also means that concerns about bias should be front and center. I really hope nobody uses Jev to rank job applicants—that floating point number could conceal all manner of unseen bias baked into the models, and experimentally picking that bias apart is going to be a tricky business.

Simon also acknowledges that LLM explanations aren't guaranteed to be useful or accurate either.

But I am not convinced that, let's say, the verbose answers of LLMs offer any more transparency than Jev does. An LLM can give a convincing justification for its answer, but that justification is generated text — not necessarily a faithful account of what caused the model to choose that answer. A plausible explanation and an auditable decision process are not the same thing.

I think transparency has to come from the design of the surrounding system instead. 

You should not give Jev a résumé and a job description and ask, “Is this applicant a good fit?” That hides too many separate judgments behind one number. Instead, you could ask narrow questions: Does the applicant have experience leading a team? Do they know Go? Do they speak Spanish? Your code can then combine those answers using explicit rules and weights.

The individual judgments are still produced by a black box. They may still be wrong or biased, and they need to be tested. But the overall decision is decomposed into named criteria that can be inspected, evaluated, and changed independently. You can see which judgments contributed to the outcome and exactly how your code combined them. 

To me, that is more meaningful transparency than asking an LLM to explain its answer after the fact.


## The real win for Jev: Looking beyond LLMs

A nice side effect of Jev is that it makes people look beyond generative LLMs.

The LLM revolution brought a lot of people into AI who didn't have any machine learning or AI background before, and that is truly great. Democratization is exactly what we need in AI and machine learning. 

And it makes sense that LLMs became the default. One API can handle translation, classification, extraction, and code generation. You don't need to know which model architecture fits your problem or collect a dataset before trying an idea. That convenience is a huge part of their appeal.

But it also means that, for a lot of people, AI is equivalent to LLMs. Every task is a nail to be hammered by an LLM. 

But generating text is not always what the application actually needs. Sometimes you need to extract entities, where something like [GLiNER](https://github.com/urchade/GLiNER) may be enough. Sometimes you need to rank search results, where [a dedicated reranker](https://huggingface.co/BAAI/bge-reranker-v2-m3) may be a better fit. Sometimes you already have labeled data and a fine-tuned classifier built on something like [ModernBERT](https://huggingface.co/answerdotai/ModernBERT-base) is all you need.

The question is not just which model is smartest, but which model gives you the right behavior at the right cost, latency, and deployment constraints.

What I like about Jev is that it makes this choice feel relevant again. Instead of immediately asking “How do I prompt an LLM to do this?”, maybe we start by asking “What kind of prediction does my application actually need?” Even if Jev isn't the answer, that is a useful change in how we think about building with AI.

## It feels so much more useful to me

And maybe the most important part for me is that Jev gets my creative juices flowing again. 

I was in kind of a ditch before in terms of building stuff and exploring things, because LLMs made it kind of pointless to build anything, because you can build everything. There is no struggle, there are no restrictions, and there is no meaning, almost. 

Jev introduces a new (very constrained) primitive to build upon. It welcomes composition, decomposition and experimentation. 

*What is it good at? What is it not good at? How can I formulate that task so that Jev can do it?* 

The API is also very accessible, and the model is cheap and fast, so that experimentation has a very low entry bar. 

Even more so with agents nowadays.

I can describe an idea to them and have a working prototype a few minutes later. I can see whether it kind of works and then scrap the prototype and build it up again slowly together with LLMs to really understand what is going on. 

Maybe this is another reminder that constraints can be good for creativity. Having a small primitive with clear limits gives me boundaries to explore and pieces to combine. It's almost like a new Lego brick.

For me, coding has never been only about getting a working application at the end. It's also a form of creative self-expression — a way of exploring ideas and making something my own. Other people may approach it differently, and that's fine.

But that is the part I had been missing, and somehow Jev has made room for it again.
