---
title: "Few-shot DSPy optimizers explained"
date: 2025-07-26T15:27:52+01:00
draft: false
excerpt: Let's look at how some of the basic DSPy optimizers work...
image: dspy-optimizers.png
---


![Few-shot DSPy optimizers explained](/images/dspy-optimizers.png)

[DSPy](https://dspy.ai) is an awesome library for building [compound AI systems](https://bair.berkeley.edu/blog/2024/02/18/compound-ai-systems/) in Python. But it also comes with a lot of jargon and special terminology that makes diving into the library quite confusing for newcomers.

But I truly believe that the ideas behind all of the jargon are actually simple and easy to understand.

If you've tried diving into DSPy documentation, you've probably encountered terms like `traces`, `bootstrapping`, and `teleprompters` and wondered what they actually mean. Let me show you.

A good way to dive into the world of DSPy jargon is to look at what some of the optimizers do.

Specifically, I want to dive into these three optimizers: `LabeledFewShot`, `BootstrapFewShot` and `BootstrapFewShotWithRandomSearch`, since they all build upon each other and are a good way to explain what **“traces”** (or trajectories) and **“bootstrapping”** are.

So let’s get started.

## Examples

Actually, before we dive in, we need to clarify some additional terminology first.

When I talk about “examples”, I mean Input/Output pairs. I usually wrap them in a `dspy.Example()` object so they play nicely with the rest of the library, but that’s entirely optional.

```python

dataset = [dspy.Example(question="what is the meaning of life?", answer="42").with_inputs("question"), ...]
```

Okay, but now let’s really get started.

## LabeledFewShot

This one is actually the easiest to understand, but it’s also the underlying mechanism for everything to come, so stay with me.

`LabeledFewShot` samples `k` examples (input/output pairs, hence *Labeled*FewShot) from your dataset and puts them into the prompt as `demos` (or examples). It will only add the fields that you specified in your examples to the prompt - usually the initial input and the final output. It does not create any intermediate values that may lead to the final output (we'll come to this idea later).

Of course that’s better than nothing to nudge your LLM pipeline in the direction, but we can do better. But what if we could give the LLM more than just input-output pairs? What if we could show it the reasoning path? This is where `traces` and `bootstrapping` comes in.


## BootstrapFewShot

To understand what this optimizer does, we need to understand what a “trace” is and what “bootstrapping” in the context of “traces” means.

A trace is the sum of all inputs and outputs of your DSPy program. It’s basically the path your input takes to become the output, which each station in between.

Let’s make it concrete.

```python
class MathWordProblemSolver(dspy.Module):
    def __init__(self):
        super().__init__()
        # Step 1: Understand the problem
        self.problem_analyzer = dspy.ChainOfThought("word_problem -> key_info, unknown_variable")

        # Step 2: Set up the equation
        self.equation_builder = dspy.ChainOfThought("key_info, unknown_variable -> equation")

        # Step 3: Solve the equation
        self.solver = dspy.ChainOfThought("equation -> solution_steps, answer")

        # Step 4: Verify the answer
        self.verifier = dspy.ChainOfThought("word_problem, answer -> verification")

    def forward(self, word_problem):
        # Step 1: Analyze the problem
        analysis = self.problem_analyzer(word_problem=word_problem)

        # Step 2: Build equation
        equation_result = self.equation_builder(
            key_info=analysis.key_info,
            unknown_variable=analysis.unknown_variable
        )

        # Step 3: Solve equation
        solution = self.solver(equation=equation_result.equation)

        # Step 4: Verify answer
        verification = self.verifier(
            word_problem=word_problem,
            answer=solution.answer
        )

        return dspy.Prediction(
            key_info=analysis.key_info,
            equation=equation_result.equation,
            solution_steps=solution.solution_steps,
            answer=solution.answer,
            verification=verification.verification,
            unknown_variable=analysis.unknown_variable
        )
```

This is a DSPy module that solves math word problems (like the ones you know from school). It first analyzes the question, identifies the key info as well as the unknown variable, then it turns this info into an equation, solves it and verifies the answer.

Now a trace is the record of the input, output and intermediate steps of a call to this module:

```
Problem: Sarah has 15 apples. She gives 3 apples to each of her 4 friends. How many apples does she have left?

🔍 Step 1 - Problem Analysis:
Key Info: Sarah starts with 15 apples. She gives 3 apples to each of 4 friends, totaling 12 apples given away.
Unknown: The number of apples Sarah has left.

📝 Step 2 - Equation Setup:
Equation: 15 − 12 = 3

⚡ Step 3 - Solution:
Steps: 1. Start with the larger number: 15.
2. Subtract the smaller number: 15 − 12.
3. Perform the subtraction: 15 − 12 = 3.
Answer: 3

✅ Step 4 - Verification:
Verification: The provided answer of 3 matches the correct calculation (15 − 12 = 3), so the answer is verified as correct.
```

(Of course this is a little embellished with all of the emojis for presentation purposes, but you get the point)

All of these intermediate inputs and outputs lead to the output, but you don’t necessarily have labels for them. You may only have labels for the input (`word_problem`) and output (`answer`).

But all of these intermediate steps are of course great signals for the LLM to know how to arrive at the final answer. It basically shows the "thought process" if you will.

This is where “bootstrapping” comes into play.

I think of bootstrapping this way:

You sample an `Example` from your dataset, put it through your module and if it arrives at the correct output (measured by a metric, in the case above just something like `prediction == answer`), you put the whole `trace`, all of the intermediate steps, into the prompt as a few-shot example - or `demo` as DSPy calls it.

It basically shows the model what kind of intermediate outputs may lead to the right output, thus giving the model more signal than just the right input and output—it also shows what intermediate steps led to the correct answer.

The `max_rounds` parameter defines how often the model loops through the dataset and tries to come up with a trace that leads to the right output. With `max_rounds=3` the algorithm will loop through the whole dataset up to `3` times to come up with working traces.

But `BootstrapFewShot` also adds “normal” input-output-only demos to the prompt. The amount of “normal demos” in the prompt is controlled by the `max_labeled_demos` parameter.

If your DSPy program only consists of a single `Predict` module then there is no difference between `LabeledFewShot` and `BootstrapFewShot` since there is nothing to "bootstrap". Your program doesn't produce any intermediate or additional values that could help the LLM to understand how to arrive at the correct output.

## BootstrapFewShotWithRandomSearch

This optimizer enhances BootstrapFewShot by searching for the perfect bootstrapped and non-bootstrapped few-shot example set. It samples examples randomly a bunch of times and evaluates the constructed few-shot set on a validation dataset. The number of programs or few-shot sets evaluated can be controlled with the `num_candidate_programs` parameter.

What’s not documented is that additionally to the number of candidate programs it also evaluates three additional programs:

1. without any few-shot examples (“zero-shot”)
2. `LabeledFewShot`
3. `BootstrapFewShot` with un-shuffled training dataset

So if you specify `num_candidate_programs=16` you actually end up with `16 + 3 = 19` programs. This tripped me up at the beginning.

Anyway.

So this optimizer shuffles your training dataset and repeatedly applies the `BootstrapFewShot` optimizer on it, every time with another subset of your training dataset. Then it evaluates it on your training dataset (or a separate eval dataset) and records the eval score. In the end it returns the program with the highest eval score.

So it just randomly searches for the best combination of few-shot examples basically - hence the name.

I'm not really happy with the current implementation of this because it evaluates the current program on the training set including the examples it added to the prompt, which are obviously trivial to solve if they are also in the prompt. This may lead to overly optimistic evaluations, especially with smaller datasets. A better approach would be to remove the examples that were added to the prompt from the evaluation dataset, similarly to what cross validation does.

## When to use which optimizer?
This question isn't easy to answer and I doubt that there is a single correct answer. It depends (as so often).

I would use `BootstrapFewShot` if you only have very little "training data" (maybe 10-15 examples).

If you have more examples, maybe 30 - 50, that you can use for optimization, then you can experiment with `BootstrapFewShotWithRandomSearch`. I did some experiments with varying numbers of examples for optimization and that was the amount of examples where you start to see generalizable optimization results. But - as always - YMMV.

Also I wouldn't tamper too much with the default arguments to the optimizers. In my experience the default values are usually good enough as a starting point and optimizing the optimizer parameters should probably be the last thing you do to squeeze out some more performance. There is usually lower hanging fruit to be had first.

## Conclusion
These three optimizers give you a great head start on the most fundamental DSPy concepts and a lot of the advanced optimizers like MIPRO or SIMBA either use a variation of the optimizers above or at least they also use the terminology introduced above.

Love talking about building things with AI? Hit me up on [X aka Twitter](https://x.com/rasmus1610).
