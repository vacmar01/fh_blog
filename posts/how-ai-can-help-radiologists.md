---
title: "How AI Can Really Help Radiologists"
date: 2022-11-06T18:53:57+02:00
draft: false
---

*„People should stop training radiologists now“* reads a quote by Geoffrey Hinton from 2016, one of the godfathers of Deep Learning.  Curt Langlotz, a radiologist from Stanford University is not so pessimistic: *“AI won’t replace radiologists, but radiologists who use AI will replace radiologists who don’t”*. But not only are we radiologist still being trained in 2022, The number of AI tools I use in my day-to-day work as an academic radiologist is negligible. 

Most diagnostic medical imaging AI tools that come to market right now are not geared towards radiologists, but towards other medical professionals that have to deal with medical images. In this post I want to explore how an AI tool should look that would really help radiologists in their day-to-day workflow and has a high chance of actual adoption in a radiology department.

Most diagnostic AI tools right now are targeting straight-forward diagnostic tasks like detection of pulmonary embolism or pneumothorax in a chest x-ray. While these tools may have their merit in a triage setting (that’s how [aidoc](https://www.aidoc.com/) positions their product) or a setting where no trained radiologists is available (think of developing countries), for experienced radiologists these well circumscribed, straight-forward diagnostic tasks are trivial. If you show a computed tomography pulmonary angiogram (CTPA) to a radiologist and ask him whether this patient has a pulmonary embolism, she can usually answer this question in 10 seconds or less with a very high sensitivity and specificity ([source](https://pubmed.ncbi.nlm.nih.gov/16738268/)). The same holds true for the many other straight-forward tasks that AI claims to do better than radiologists. 

The real benefit of diagnostic AI tools for radiologists comes when the AI tools solve tasks that are either very time consuming or very hard, even for trained radiologists. One example of a time-consuming task would be the detection of new multiple sclerosis lesions in a brain MRI of a patient that already has a high number of multiple sclerosis lesions. A task that is really hard, even for experienced radiologists, may be the reliable estimation of brain atrophy from brain MRI scan. 

AI applications get even more interesting for radiologists if they enable diagnostic insights that are not possible without an AI algorithm. A recent challenge on Kaggle.com tasked the participants with the development of an algorithm that can classify malignant brain tumors (glioblastomas) based on the presence of a specific gene sequence (MGMT promoter). The winner developed an algorithm with a respectable area under the curve (ROC AUC) of 0.62. To my knowledge there is no known imaging sign that would enable a human to do the same classification. 

Physicians are inherently inert and lazy. Your AI application has to be highly integrated into the normal workflow of the radiologist, otherwise it will not be used. And a tool that’s not used does not provide value. To exaggerate: If you need to export the exam manually as DICOM from the PACS and then open it in your AI application, then the time gain your tool promises is gone. The question of how your tool fits into a typical radiologist workflow should dictate the whole product design and should be no after-thought. 

Another thing to consider is the presentation of the results. We as radiologists are visual people. We like to look at pretty pictures. AI tool manufacturers should think really hard about how they want to present their results to the radiologist. A table with many numbers might not be the best way. The results should be visualized. An integration of the results into the analyzed images, maybe as an overlay, is usually the most straight-forward way.

![](https://miro.medium.com/max/1400/1*y-uycKblYfNfafDr_vGbKA.png)
Source: [@DrHughHarvey](https://twitter.com/DrHughHarvey)

The actual diagnostic task is not the bottleneck in radiology and something that we as radiologists actually enjoy. But radiology is much more than just reading exams. In my opinion an often overlooked, but for me as a radiologist very tiresome area where AI could be tremendously helpful is what I like to call “backoffice jobs”. These are things like: 

* Image reconstruction
* Image registration
* Intelligent sourcing of relevant prior studies
* Intelligent hanging protocols of studies in the PACS
* triaging of imaging requests and scheduling of examinations
* Intelligent optimization of contrast agent protocols based on patient characteristics 

What all of these “backoffice tasks” have in common is that they need a tight integration with CT/MRI scanners, the PACS or the scheduling software used. This presents a major challenge for independent AI manufacturers. Many MRI/CT scanner and PACS vendors are already working on such solutions, since they have access to the protocols and integrations. This leads to a fragmented landscape of tools since every vendor works on its own tool. A standardized protocol that allows AI tools to communicate with the PACS or the CT/MRI scanners would be helpful for the independent development of these tools.

I’m sure someday there will be an AI algorithm that can read a radiological study from end to end and produce a human readable report of it. But this is still a long way off for several reasons. The tech is not there yet. Until then there is a huge opportunity for AI tool startups to make the life of us radiologists easier. 

---

Follow me on [Twitter](https://twitter.com/rasmus1610) and don't miss my next post.

