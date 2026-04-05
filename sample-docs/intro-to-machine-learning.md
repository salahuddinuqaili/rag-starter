# Introduction to Machine Learning

Machine learning (ML) is a way of teaching computers to recognize patterns in data
and make predictions without being explicitly programmed for every scenario. Instead
of writing rules by hand, you show the computer thousands of examples and let it
figure out the rules on its own.

## Supervised vs. Unsupervised Learning

In supervised learning, you give the computer labelled examples — inputs paired
with the correct answers — and it learns to predict the answer for new inputs.
Spam detection is a classic example: you feed the model thousands of emails labelled
"spam" or "not spam," and it learns which words, phrases, and patterns indicate
junk mail. After training, it can classify emails it has never seen before.

In unsupervised learning, there are no labels. You give the computer a pile of data
and ask it to find structure on its own. Customer segmentation is a common use case:
you provide purchase histories for 50,000 customers, and the algorithm groups them
into clusters — frequent buyers, bargain hunters, one-time visitors — without you
telling it what the groups should be. You discover the categories after the fact.

There is also reinforcement learning, where an agent learns by trial and error in
an environment, receiving rewards for good actions and penalties for bad ones. This
is how game-playing AIs and self-driving car simulations work, but it is less
common in everyday business applications.

## Training Data and Why Quality Matters

A machine learning model is only as good as the data you train it on. If your
training data is biased, incomplete, or noisy, the model will learn those flaws
and reproduce them confidently. A hiring model trained only on data from the last
decade will inherit every bias present in a decade of hiring decisions.

Quality training data is labelled accurately, covers the full range of cases the
model will encounter in production, and is large enough for the model to
generalize rather than memorize. Collecting and cleaning training data typically
takes more time than building the model itself.

## Overfitting

Overfitting happens when a model performs brilliantly on the data it trained on
but fails on new, unseen data. Think of it like a student who memorizes every
answer in a practice exam booklet but cannot solve a problem worded differently on
the real test. The student learned the specific answers, not the underlying
concepts.

You detect overfitting by splitting your data into a training set and a test set.
Train the model on the training set, then measure its accuracy on the test set.
If training accuracy is 99% but test accuracy is 60%, the model has memorized
rather than generalized.

Common remedies include using more training data, simplifying the model (fewer
parameters), and techniques like dropout and regularization that deliberately
introduce noise to prevent memorization.

## Real-World Applications

Machine learning is already embedded in tools you use daily. Recommendation engines
on Netflix and Spotify predict what you want to watch or listen to next based on
your history and the behaviour of similar users. Fraud detection systems at banks
flag unusual transactions in milliseconds by comparing them to patterns of known
fraud. Medical imaging models help radiologists spot tumours in X-rays and MRIs,
sometimes catching details that the human eye misses.

These applications share a common thread: they involve tasks where the volume of
data exceeds what a human can process manually, and where patterns exist but are
too complex to capture in hand-written rules. That is where machine learning
thrives.
