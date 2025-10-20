---
title: "The Not-so Bitter Lesson"
date: 2025-10-20T15:27:52+01:00
draft: false
excerpt: How tinygrad helped me finally understand what Sutton meant
---

Have you heard about The Bitter Lesson? If you are on Twitter and follow some ML/AI people, I bet you have. 

If you haven't: It is a [blog post by Richard Sutton](http://www.incompleteideas.net/IncIdeas/BitterLesson.html), a Canadian computer scientist, who wrote one of *the* books about reinforcement learning. 

Sutton's core argument is simple: general methods that leverage search and compute outperform domain-specific solutions. By "search," he doesn't mean information retrieval - he means using learning algorithms to explore possible solutions or strategies. His go-to example is computer chess: early engines relied heavily on chess expertise to evaluate positions, while AlphaZero knew only the basic rules and learned by playing itself, eventually surpassing any human player.

This lesson is "bitter" because it suggests our clever insights don't matter. Our domain-specific knowledge gets crushed by what looks like "dumb brute-force search and compute." If you're an engineer, this naturally raises an uncomfortable question: what's the point of us?

## The Click

For a long time, I didn't really understand Sutton's point. What does it mean to solve problems using search and compute? What is the role of engineers then? Are we just supposed to prompt a LLM and hope for the best? That can't scale.

My aha moment came from an unlikely source: [`tinygrad`](https://github.com/tinygrad/tinygrad). It's a Python library similar to PyTorch but much simpler on the surface. I think George Hotz initially built it as a toy project after watching Andrej Karpathy create micrograd, but it evolved into a solid tensor library that runs LLMs efficiently on different hardware through clever optimizations.

George's blog post ["Can tinygrad win?"](https://geohot.github.io//blog/jekyll/update/2025/07/06/can-tinygrad-win.html) made everything click. He lays out his vision for the library: the entire stack of making code run fast on hardware is fundamentally a search problem across multiple layers — searching for better scheduling algorithms, faster GPU kernels, all of it. The task of the library is to "Expose the underlying search problem spanning several orders of magnitude." and then "Apply the state of the art in search. Burn compute.". 

That's when I finally understood what Sutton meant. Like in computer chess, raw compute and effective search will beat manually crafted solutions. 

But the key insight is this: someone still has to expose that search problem. Someone has to frame it correctly.

In this post, I'll show you why our work as engineers still matters, just differently. The Bitter Lesson isn't bitter at all - it's a blueprint for better engineering. And the pattern of search & compute appears everywhere once you know what to look for.

## The Framework

For me, The Bitter Lesson is all about building effective search systems. Again, not search in the sense of information retrieval, but in the sense of allowing raw compute to explore a space of solutions effectively.

For that we need three core components: 
1. An effective problem formulation that exposes the right parameters in a way that different algorithms can dig into it.
2. A way to evaluate possible solutions (evals) and provide feedback to the search mechanism. 
3. A way to define constraints that a solution has to satisfy (memory, time, specific form etc.)

Our job as engineers is to build these three components. We design the problem-specific, scalable infrastructure that enables search to work. Then we gtfo and let compute do what it does best.

But don't you worry, there is still place for your precious domain knowledge, even in The Bitter Lesson, but you should use it elsewhere:

Use your domain knowledge to:

* Design problem representations (make search tractable)
* Build evaluations (capture what matters)
* Set constraints (avoid unsafe regions)
* Initialize search (warm start)

And use search to:

* Explore solution space
* Find non-obvious patterns
* Exceed human intuition
* Scale the solution with compute

Sound familiar? We've done this before — moving from punch cards to text-based code was the same kind of shift. And now we're building harnesses and guardrails (and [RL environments](https://www.primeintellect.ai/blog/environments)) that define the bounds of desired solutions rather than crafting the solutions directly.

## The Examples

It's fascinating to see where these themes come up, besides `tinygrad`. 

If you follow me on [Twitter](https://twitter.com/rasmus1610), you might know that I'm a huge fanboi of DSPy - a declarative library for "programming not prompting" LLMs. And DSPy embodies the approach described above by separating problem definition from solution strategy. Omar Khattab, the creator of the library, actually gave a talk called ["On Engineering AI Systems that Endure The Bitter Lesson"](https://youtu.be/qdmxApz3EJI?si=P8CFiY1gD1lCMFoG) at this year's AI Engineering conference in San Francisco. Interestingly, his vision of DSPy mirrors George Hotz's vision for tinygrad: provide the right level of abstraction, then let search & compute do its thing. 

One key mechanism here is [DSPy's signatures](https://dspy.ai/learn/programming/signatures/). A DSPy signature is like a function signature in the sense that you specify your inputs and the shape of your desired outputs. It gives you the flexibility to go from input to output however you want. Sure, currently this "however" means LLMs, but just because they are the most flexible piece of computing we currently have. But if some other paradigm (or even a newer LLM) comes around the corner, your DSPy modules are very easy to adapt to it.

This search & compute principle is also captured beautifully in a talk I stumbled upon some weeks ago. [Rens Dimmendaal](https://rensdimmendaal.com/) on the [Solveit Discord server](https://solve.it.com) pointed me to [a talk by Raymond Hettinger](https://www.youtube.com/watch?v=_GP9OpZPUYc) aptly titled "Modern solvers: Problems well-defined are problems solved". Just the title captures perfectly what I think The Bitter Lesson is all about. 

One of the topics in his talk, SAT solvers, shows how problem formulation may become the critical engineering work. For those who don't know what a [SAT solver](https://en.wikipedia.org/wiki/SAT_solver) is, go and read the Wikipedia page. I'm kidding. It's a piece of software which can solve boolean algebra problems very effectively - and you would be surprised how many problems can be formulated as boolean algebra problems. But - without going into too much technical detail (you can really read the wikipedia page - it's linked above) - it expects the input to be in a very specific logical form, called the [conjunctive normal form (CNF)](https://en.wikipedia.org/wiki/Conjunctive_normal_form). And it turns out that just defining your problem in CNF is often surprisingly tricky. But once you got there, a modern SAT solver gives you the solution very fast, even for very complex problems.

It's also no coincidence that [AI evals](https://maven.com/parlance-labs/evals) have become such a hot topic for building LLM apps recently (h/t [Hamel Husain](https://hamel.dev)). When you're iterating on LLM applications - whether manually or with prompt optimizers - you're essentially searching through a solution space. But unlike a binary classifier where you can rely on simple metrics like accuracy, LLMs have massive output spaces that are much harder to evaluate. Here, building robust evals becomes critical engineering work: you need to define what "good" means for your specific problem, build systems to measure it reliably, and scale that evaluation. This is another instance of building the harness — the infrastructure that lets search & compute work effectively.

But this principle even extends to the physical world. [Proxima Fusion](https://www.youtube.com/watch?v=3Nr__6DDk6I) optimized their stellarator fusion reactor design through numerical simulation—defining the physics constraints, then letting compute search the design space before building the hardware. [AlphaFold](https://alphafold.ebi.ac.uk/) does something similar for proteins: define the structure prediction problem, set up physical constraints, then let search explore conformational space.

## The Conclusion

Look, maybe I'm fooling myself here. Maybe Sutton is right all the way down, and eventually even problem formulation gets automated. Maybe we'll all end up sipping synthetic mojitos in the metaverse while AGI does everything. But we're clearly not there yet - and I don't think we will be anytime soon. 

So for now, when I think of The Bitter Lesson, I'm not depressed because we software engineers will become obsolete, but I'm excited because it points to what we should focus on: Building scalable systems that leverage search and compute. It's about moving up an abstraction level, building harnesses instead of solutions and defining problems instead of hardcoding solutions (hardcoding is rarely a good thing it seems). 

And in my mind, that sounds just as interesting.