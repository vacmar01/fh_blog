---
title: "We Don't Build the Machines Anymore"
date: 2026-01-16T12:00:00+01:00
draft: false
image: we_dont_build_machines_anymore.webp
excerpt: We design the machines. We don't build them anymore. I'm still not sure how I feel about that.
---

![Software Engineering, 2026](/images/we_dont_build_machines_anymore.webp)

I've had an idea for a web app sitting in the back of my mind for years. A simple thing — you print a QR code, hang it at a party, and guests scan it to upload their photos to a shared album. Like many side projects, it stayed there. I was always too lazy to actually code it.

Then at the start of January 2026, I started using Claude Code and OpenCode more and more. And everything changed.

Instead of writing code line by line, I found myself doing something different: I created a product requirements document (PRD), turned that into a technical specification, broke the spec down into distinct task packages (epics, if you're into agile terminology). And then... the AI built it.

![OpenCode workflow](/images/opencode.webp)
*Is that what we've come to?*

My job became reviewing the work, catching bugs, steering the ship. I wasn't typing out the code anymore — I was designing the app on a higher level.

And that got me thinking: is this what software engineering is becoming?

## The Mechanical Engineering Analogy

Because it reminded me of something familiar — the way mechanical engineers work.

Mechanical engineers don't build the machines they design with their bare hands. At least from what I understand — and I'm not a mechanical engineer, so take this with a grain of salt — they spend their days designing systems on a higher level, building prototypes to test hypotheses, calculating specific parts in detail. Once the design is validated, they hand it off to technicians or machines which actually assemble the thing. Screw in the bolts, wire up the electrical boards. The engineer's job then shifts to observing, troubleshooting, and refining.

That workflow felt very familiar.

With my web app, I was doing exactly this: designing the system, writing specifications, doing small experiments to test ideas, then handing the actual assembly off to the AI. When something broke, I'd diagnose the problem and guide the fix. The creative, high-level work was mine. The typing — the "assembly" — was delegated.

Maybe software engineering is evolving into something similar. Just operating at a higher level of abstraction, the way other engineering disciplines have for decades.

## A Brief History of the Split

Here's the funny thing: this separation between "design" and "assembly" isn't new in software. It's actually how software development *started*.

In the early days of computing — the 1950s and 60s — there was a clear distinction. Mathematicians and engineers would design the programs, and then programmers (often women, by the way) would translate those designs into punch cards. The implementation work was considered clerical. You had the thinkers, and you had the typists.

So what happened? Why did these roles merge?

A few reasons. First, software is uniquely malleable — unlike a bridge or an engine, you can change code instantly at almost zero cost. Second, the feedback loops are incredibly tight — you write something, you run it, you see if it works. This made separating design from implementation inefficient. By the time you handed off a spec, waited for implementation, and got something back, you'd lost all that rapid iteration. Third, as programming languages became more expressive, the "typing it out" part required more and more judgment. Writing Python isn't like punching cards.

So the roles merged. And it made sense. For decades.

But now AI changes the equation again. Why? Because the feedback loop doesn't break anymore. The AI responds in seconds. I describe something, it builds it, I see the result, I adjust — all in minutes. The malleability is still there, the tight iteration is still there. It's just mediated through conversation instead of typing.

So in a way, we're coming full circle. The split is back — but faster.

## What This Means for the Craft

If this shift continues, what changes for us as software engineers?

I think the skills that matter will shift toward the front and back of the process. On the front end: understanding problems deeply, thinking through architecture, writing clear specifications, asking the right questions. On the back end: reading code critically, spotting bugs and edge cases, knowing when something "smells off" even if you didn't write it yourself.

What becomes less central? The middle part — the raw typing, the syntax, the boilerplate. The assembly.

This doesn't mean coding knowledge becomes irrelevant. A mechanical engineer still needs to understand materials, forces, and manufacturing constraints — they just don't operate the lathe themselves. Similarly, I still need to understand how authentication works, how databases scale, why certain patterns exist. I just don't need to type out every line myself.

In some ways, this is liberating. That web app I'd been putting off for years? After just a couple of days it was in a much better state than I would have gotten it in months of manual coding. Not because I'm thinking more clearly now — but because the activation energy dropped. Things I *could* have done before, but didn't because they felt like too much work for a side project — transcoding videos on upload, converting images to web-friendly formats — I just... do them now. The barrier went from "spend a weekend learning FFmpeg" to "describe what I want and review the result."

I do still learn how these things work, at least on a higher level. But I'll come back to that — because I'm not sure that kind of learning is the same as the manual struggle I had before.

## Where Does This Stabilize?

So if we keep going up the abstraction chain... where does it stop? Does it stop?

Right now, I'm reviewing code, catching bugs, steering the AI at the implementation level. But what if that becomes unnecessary too? Maybe next year (next quarter?!) I'm just reviewing *features*, not code. The year after that, maybe I'm just describing *products*.

Omar Khattab — the guy behind DSPy — talks about this a lot. His argument is that the remaining hard problem is *specification*. Being able to describe what you want precisely and expressively enough that the AI can build it. If you can do that, the implementation becomes a solved problem. It doesn't matter if you're specifying at the feature level or the code level — the skill is the same.

Maybe he's right. And if you think about it — programming was always about specification. Code was just a very precise, very productive way of expressing what you want. A good mixture of being expressive and being exact. So maybe the core skill isn't changing at all. Only the medium is. From punch cards to assembly to Python to... structured prompts? PRDs? DSPy modules? Whatever comes next.

Maybe the future software engineer is just someone who's really good at specifying things — which is what we always were. At thinking clearly about requirements, edge cases, constraints. The "how it works underneath" becomes as irrelevant as knowing how transistors work is for most programmers today.

But I'm not sure.

Can you really specify well without understanding the underlying systems? When I write a spec, I'm drawing on years of knowing how authentication actually works, how databases fail, why certain patterns exist. That knowledge shapes what I think to specify in the first place. Without it, would I even know the right questions to ask?

Or maybe I'm wrong. Maybe that's just cope.

Because honestly? I *like* thinking at the software level. I like the deep technical work. And I'm a bit sad — and yeah, worried — that this thing I enjoy, this thing that's also been a pretty good career, might be going away.

I don't have a clean answer here. Maybe the abstraction keeps rising and we adapt. Maybe there's some natural floor where human judgment remains essential. Maybe I'm just in denial.

## The Learning Problem

There's one more thing that worries me: how do we learn in this new world?

I learned to code by typing things out, by struggling through authentication flows and database schemas and HTTP quirks. That struggle *was* the learning. If newcomers to programming start at this higher level of abstraction, will they develop the deep understanding needed to steer the AI in the right direction? You can't be a good architect if you don't understand how buildings actually stand up.

And it's not just newcomers. I worry about my own growth too. I know how to code — but now I'm always tempted to outsource the hard details to the AI. Will I atrophy?

There's a tension here between short-term and long-term thinking. Exploration versus exploitation. Using AI extensively is clearly the best short-term strategy — you move faster, ship more, build things you wouldn't have built otherwise. But if you never struggle through the hard parts yourself, do you stop growing? Are you taking on a kind of personal debt, borrowing against future capability for present speed?

Or maybe not. Maybe you still learn — just differently. Maybe there's a middle ground I haven't found yet. I honestly don't know.

Maybe it's like other engineering disciplines — students still learn fundamentals by hand in university before they ever touch professional tools. Maybe we need a clearer distinction between *learning mode* and *production mode*. Maybe the answer is something else entirely.

What I do know is that the way we work is changing. Whether that's good or bad probably depends on how intentionally we adapt to it.

---

Wanna talk? Hit me up on [Twitter](https://twitter.com/rasmus1610).
