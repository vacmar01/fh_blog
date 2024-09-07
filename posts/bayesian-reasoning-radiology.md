---
title: "Diagnostic Tests & Probabilities"
date: 2020-12-11T13:04:06+01:00
draft: false
---


> „Science is a way of trying not to fool yourself. The principle is that you must not fool yourself, and you are the easiest person to fool.“ - Richard Feynman  


We are taught very little about how to decide what to do with our patients based on the evidence at hand. Even if we often pretend to do so, we can never be 100% certain what the cause of our patient's symptoms is. We can just use tests and examinations to make sure we are a little bit more certain than before.

But an incomplete understanding of the nature of diagnostic tests and probabilites does not only lead to critical mistakes with far-reaching consequences for the patients but it also results in wasted resources. 

I will present a mental model that can be used to improve these decisions under uncertainty. It is called **Bayesian reasoning**.

If we look closely, making a diagnosis has a lot in common with the [scientific method](https://www.youtube.com/watch?v=EYPapE-3FRw): 
1. We make a hypothesis (suspected diagnosis) based on patient demographics and clinical symptoms.
2. We gather evidence for or against our hypothesis with diagnostic tests.
3. We then re-evaluate our initial hypothesis based on the results of the diagnostic test and decide what to do next.

How certain we are of your diagnosis can be expressed as a probability that our hypothesis is true. As an example, we can think: „50 % of patients with this clinical appearance and this age have an appendicitis“.

Bayesian reasoning means updating your existing beliefs - your hypothesis or suspected diagnosis - based on new evidence using tools of math and logic. Bayes theorem formalizes this updating and provides a formula that gives you the „post-test probability“ that your hypothesis is true given the „pre-test probability“.

We can use Bayesian reasoning to understand what the actual aim of a diagnostic test is: The aim of a diagnostic test is to alter the degree of certainty that the patient has a particular condition. A diagnostic test must make us certain enough that a patient has a specific condition or not so that we know how to proceed further. A diagnostic study must have the possibility to change the patient's course, otherwise it is useless. If a diagnostic test has no consequence, we need to think really hard why we think we need it in the first place.
		
It is important to note that the probability that a patient has a certain diagnosis after a test is not the same as the sensitivity of the test. The „post-test“ probability is highly dependent on the probability that the patient has a particular diagnosis before we conducted the test, the so called „pre-test“ probability. Only with the sensivity and the pre-test probability together we can derive the „post-test“ probability. That is extremely important and often neglected, even by experienced physicians. Ignoring the pre-test probability leads to an overestimation of the „post-test“ probability and makes us more confident in our suspected diagnosis than we should be.

What follows is that a positive diagnostic test can mean different things based on the pre-test probability. If the pre-test probability is low, the probability that a positive test is actually a false positive is very high. An often cited example are breast cancer screening programs, where the pre-test probability equals the populations’ prevalence of breast cancer and is therefore rather low. Not knowing how to interpret a positive test in this circumstance leads to unnecessary worrying of the patient and may cause physical harm due to unnecessary invasive biopsies.

It is important to remember that the pre-test probability varies in different settings. It is higher in tertiary care (e.g. in a university hospital) than in primary care, because the patients have been preselected accordingly. Only those patients for whom there is a strong suspicion of a disease are referred to a tertiary care center.  This is phenomenon called _„referral bias“_. 

Not remembering these facts about the nature of tests and probabilities can lead to critical mistakes in the management of your patients. But thinking in probabilities is hard and even people who are trained to do it are prone to pitfalls and biases. A first step is to know what you don’t know and to acknowledge that we can never be 100 % certain. Diagnostic tests are there to lower your uncertainty. But they have to be interpreted correctly.  

A deeper understanding of probabilities and its rules will lead to a more effective and safe treatment of our patients. Therefore, I strongly believe that physicians need formal training in making decisions under uncertainty.

_Note: I made some simplifications for demonstrative purposes. Of course the outcome of a diagnostic test is not strictly binary (either positive or negative), sometimes it is something in between. Furthermore, this article focused on diagnostics. I acknowledge that medicine is not pure diagnostics, but the decision that are made at the diagnostic stage have far-reaching consequences for the course of the patient and are perfect to illustrate the concepts. And after all, I’m a radiologist._

---

Follow me on [twitter](https//twitter.com/rasmus1610) and don't miss the next post!

---



## Further reading
1. Gigerenzer G. How to Improve Bayesian Reasoning Without Instruction: Frequency Formats. Psychological Review, 102 (4), 1995, 684–704. link: https://cogsci.ucsd.edu/~coulson/203/GG_How_1995.pdf
2. Pre- and post-test probability. In: Wikipedia. ; 2020. Accessed November 15, 2020. https://en.wikipedia.org/w/index.php?title=Pre-_and_post-test_probability&oldid=949140169
3. The Value of Probabilistic Thinking: Spies, Crime, and Lightning Strikes. Farnam Street. Published May 14, 2018. Accessed November 19, 2020. https://fs.blog/2018/05/probabilistic-thinking/
4. Doust J. Using probabilistic reasoning. BMJ. 2009;339(nov03 2):b3823-b3823. doi:10.1136/bmj.b3823
5. Wood BP. Decision Making in Radiology. Radiology. 1999;211(3):601-603. doi:10.1148/radiology.211.3.r99jn35601
6. Chang P. Bayesian analysis revisited: a radiologist’s survival guide. American Journal of Roentgenology. 1989;152(4):721-727. doi:10.2214/ajr.152.4.721
7. Eddy DM. Probabilistic reasoning in clinical medicine: Problems and opportunities. In: Kahneman D, Slovic P, Tversky A, eds. Judgment under Uncertainty. 1st ed. Cambridge University Press; 1982:249-267. doi:10.1017/CBO9780511809477.019
8. Kahneman D. Thinking, Fast and Slow. [Link](https://www.amazon.com/dp/0374533555/ref=cm_sw_em_r_mt_dp_MdoZFbQCWGKNX)