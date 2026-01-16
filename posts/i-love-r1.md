---
title: I love you, R1
date: 2025-01-31T11:20:06+01:00
draft: false
excerpt: Why I think reasoning models are a huge step forward...
image: r1.webp
---

When using AI to help me with tedious research tasks, I have to trust it and be able to verify its output, because in the end, it's my name on the paper and my reputation on the line. 

I'm a researcher doing a lot of data science and applied AI stuff in the field of radiology.

While writing code to get quantitative data is what's actually fun, analyzing qualitative data is often a slog.

I'm always looking for ways to automate this part of my work. I tried to use LLMs for this several times, but I was always disappointed by the quality of their analysis and I often didn't understand why they came up with what they came up with. When it works, it does feel like magic, but when it doesn't, you have no idea why. 

Several days ago, DeepSeek, the chinese AI company, released their new LLM called "DeepSeek R1".

It's a so called "reasoning model", much like ChatGPT o1, which means it's a LLM that produces "thinking tokens" before it returns an answer. Think of it like a stream of thought of the LLM before answering the question. Before answering the prompt, the LLM produces some text where it reflects and thinks about the task at hand. But in contrast to ChatGPT o1, with DeepSeek R1 you can read these "thinking tokens". 

This reasoning step enables new capabilities like actually calculating stuff ("how many r's are in the word strawberry?") and solving more complex coding problems by self-reflecting on its ideas. 

But it also enables something else.

Before trying it out myself, I didn't really understand why these reasoning model are such a big deal. Then I did a little experiment. 

I'm currently working on a RAG application for medical question answering. To understand better why some questions are answered wrong, I went through all wrong answers and the retrieved context and took notes on what I observed. 

Then I thought: *"I could look through all of these notes myself and try to identify patterns, or I could test out this new and highly hyped LLM, called DeepSeek R1"*.

So, of course, I fed all of my notes to the model and prompted it to identify recurring patterns.

It worked beautifully. 


It identified three common problems together with examples for each problem. It even recommended ways to tackle these problems that were actually helpful. 

Then I prompted it to classify all the notes into these categories and return summary statistics. 

That's where it got fun.

In the train of thought after that prompt the LLM first defined the problem categories for itself again and then it went through every note and categorized it with commentary if it wasn't sure about what class to put the note in with a reason why it chose what category in the end. 
After that it counted what category appeared how often (admittedly it had to recount several times but it realized on its own when it messed up) and calculated the proportions of each category. You can read through all of the thought process [here](https://gist.github.com/vacmar01/14b5f96d7eb80085455980e75332fc0a).

![R1 output](/images/r1.webp)

The final answer was a table with the problem category, the count and percentage for each category as well as 2-3 key examples for every category. That was really helpful and valuable stuff. 

Reading through the thought process gave me gave me a lot of confidence in the model's classification and made the whole process very transparent.

Before, I had to trust the AI output without a great way to understand and verify its thought process. Now, I can see exactly how the LLM reached its conclusions. And often reading through the thought process of the LLM itself is helpful for your own ideas and reasoning. 

Before, It was kind of risky to use AI for your research, but with DeepSeek R1 a new era has begun.