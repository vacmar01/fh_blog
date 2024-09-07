---
title: "Kaggle RSNA Challenge 2022 Postmortem"
date: 2022-11-13T15:27:52+01:00
draft: false
---

I recently participated in my first radiology themed computer vision competition on [kaggle.com](https://kaggle.com). I did not finish well (place 559/883). My best submission was a simple baseline based on the mean of the training. It scored better than every neural net I trained. Nonetheless, I learned a lot about machine learning in general and Kaggle competitions specifically. 

Here are my learnings:

## Writing machine learning code is hard
Writing machine learning code is really hard. There are so many possibilities to induce bugs that don’t result in the notebook failing to run but in bad predictions. 
For example I accidentally applied the sigmoid function to the output of my model twice at two different places in my code and was wondering why my model produces constant outputs. Turns out taking the sigmoid of the sigmoid is not a good idea.

## Submit a dummy submission early
Without a submission pipeline in place the best model is useless in a Kaggle competition. Sometimes the submission process is trivial but more often than not it is a little bit more complicated, as it was in this competition. The test set that you had to make your predictions on was hidden. So you had to write your submission code in a vacuum without the ability to really test it. It took several days for me to get my submission code right. 
So write your submission logic early. You can submit a constant value, it doesn’t matter, but make sure it actual works and submits successfully. 

## Have a really simple baseline
This brings me to another point: Have a simple baseline. 
You don’t know how good your fancy model is if you don’t have a simple baseline in place. Maybe a simple baseline consisting of a constant prediction will perform better than your fancy deep learning model, because somethings really off there. And depending on the competition even getting a simple baseline setup isn’t trivial, maybe because reading in the data is a challenge in itself because it is so big or in an obscure data format. Or maybe the submission logic itself isn’t that easy (see point above). 

## Use every bit of data you have
Granted, I joined the competition quite late, around 1,5 months before the deadline. Nonetheless, I stubbornly used my time trying to make a 3D classification model work on unprocessed images. I completely ignored that we had segmentation data for cervical vertebrae available as well as bounding boxes for the actual fractures on a subset of the data. In retrospect it seems logical that you would use this additional data in your overall model, but I somehow stubbornly tried to make something work without this additional input data.

## Know when an approach doesn’t work and then change it drastically
I stubbornly hit my head against my 3D model approach without realizing that I might be the completely wrong approach. My local validation score was so far off of everything in the top 100 of the leaderboard that it should have made me change the course of experiments completely. But I didn’t. I tried different 3D model architectures, I tried different learning rates, learning rate schedulers and data augmentation strategies without having a strong baseline. And this is a learning too. You need to realize when a certain approach doesn’t work and then you need to change directions drastically. Optimizing hyperparameters isn’t what brings you forward.

## Read papers and previous Kaggle competition solutions
The problems you are trying to solve are rarely completely new and unique. Sure they have their unique challenges and quirks but they are probably pretty similar to something that has already been published as a research paper. Or in the case of a Kaggle competition your current competition might be pretty similar to a previous competition.
In the case of the RSNA cervical spine fracture challenge it turns out that the last RSNA hosted competitions all had similar solutions than the current one. All of the last competitions were won by sequential models and usually 3D models didn’t work that well. Also there was a very relevant research paper solving the exact same task also using sequential model: [2010.13336 Deep Sequential Learning for Cervical Spine Fracture Detection on Computed Tomography Imaging](https://arxiv.org/abs/2010.13336#). 
If I had researched a little bit better I would have seen that people are using sequential models for this kind of task and I would have tried to implement them for the Kaggle challenge too. 

## Performance does matter
Computing performance does matter. Usually I’m amused about people arguing about which new GPU is incrementally faster than the previous generation and how much RAM you need and what CPU you have available. It may come from my background of web development where people argue about database and app scalability before having more than 10 active users in their app. 
But machine learning seems to be different, especially when working with image volumes like in radiology. This data is huge and reading and decoding this data can take a lot of time.
I learned it the hard way: Reading a lot of DICOM folders simultaneously is very time consuming. It is usually a good idea to convert this data to either NifTI files or save them as Numpy arrays or PyTorch tensors directly. I spend several days figuring this out and saving the (resized) image volumes as Numpy arrays sped up my data loading by the factor of 10. 

A great resource I have found for the practicalities of training neural nets is [this blog post by Andrej Karpathy](https://karpathy.github.io/2019/04/25/recipe/).

All in all it was a great learning experience showing that actually practicing deep learning incorporates more than might meet the eye at first. I learned a lot that I can now apply to my next projects and Kaggle competitions. 
