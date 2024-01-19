---
layout: "post"
title: "Classification Report"
date: 2024-01-19
---

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>

Yesterday in a meeting, a principal software engineer bragged about a document classification model he'd worked on.
"We achieved a classification score of 99%," he said.
To the untrained ear this may sound impressive, but not to me or my manager.

My manager posed some questions in the chat:
"What are the stats on the test set?"
"How many documents of type X?"
We knew that the majority of documents were X.
Who knows after that.
Document X is so common that I'd be willing to guess that it accounts for some 90% of all document volume.
The other 10% are made up of some 50+ other document types.

But what does it matter?
Why don't we find a classification score of 99% impressive?
Two words: _class imbalance_.

# Balanced ⚖️
When you get a 99% on a test, that's impressive.
Even 95% or 90% could be considered praiseworthy.
But what about convicting criminals?

Suppose you're a judge, and you have to decide the fate of 100 defendants.
Each one can be convicted or acquitted.
Fifty of the defendants are criminals, the other 50 are innocents.
You're an experienced judge and typically know what action to take, but this time you incorrectly assess five of them.
What's your score?

$$
\begin{align}
\text{score} & = \frac{\text{number correct}}{\text{total}} \\\\
& = \frac{95}{100} \\\\
& = 0.95 \\\\
& = 95\%
\end{align}
$$

Said another way, you correctly classified 95% of the defendants.
And the "score" that we calculated is called
[accuracy](https://en.wikipedia.org/wiki/Accuracy_and_precision#In_classification).
You accurately labeled 95% of the cases correctly.

Accuracy tells us exactly that, how accurate were we?
Our rate of correct questions to total questions.
It tells us how right and wrong we were _overall_.
It does _not_ tell us _what kinds of errors_ we made.

# Confusion matrix
Turns out we marked three defendants as innocent when they should have been convicted,
and two defendants as criminals when they were innocent.

|                     | Actually Criminal | Actually Innocent |
|:-------------------:|:-----------------:|:-----------------:|
| **Marked Criminal** |        47         |         2         |
| **Marked Innocent** |         3         |        48         |

This table is commonly referred to as a [confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix),
and it allows us to understand our errors.
To do so, we define the values in our confusion matrix:

|                     |     Actual False      |      Actual True      |
|:-------------------:|:---------------------:|:---------------------:|
| **Predicted False** | True Positive ($TP$)  | False Positive ($FP$) |
| **Predicted True**  | False Negative ($FN$) | True Negative ($TN$)  |

**True Positives** and **True Negatives** are the values we labeled correctly.
**False Positives** are a [type I error](https://en.wikipedia.org/wiki/Type_I_and_type_II_errors#Type_I_error)—we incorrectly convicted an innocent.
**False Negatives** are a [type II error](https://en.wikipedia.org/wiki/Type_I_and_type_II_errors#Type_II_error)—we incorrectly acquitted a criminal.
Combining all four of these, we can define accuracy algebraically:

$$
Accuracy = \frac{TP + TN}{TP + FP + TN + FN}
$$

To better understand our judging skills, we can calculate additional metrics.
Namely, [precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall).

# Precision
> Precision can be seen as a measure of quality, ...

Precision is algebraically defined as:

$$
Precision = \frac{TP}{TP + FP}
$$

Because we have two ways of judging a defendant (a binary classification problem),
we must calculate precision from both sides:
- Where "criminal" is the positive and "innocent" is the negative,
- and where "innocent" is the positive and "criminal" is the negative.

First, where "criminal" is the positive:

$$
\begin{align}
Precision_{criminal} & = \frac{47}{47 + 2} \\\\
& = \frac{47}{49} \\\\
& \approx 0.96
\end{align}
$$

And now the "innocent":

$$
\begin{align}
Precision_{innocent} & = \frac{48}{48 + 3} \\\\
& = \frac{48}{51} \\\\
& \approx 0.94
\end{align}
$$

Our precision when convicting someone as a criminal is 0.96 and 0.94 when judging someone as innocent.
In other words,
our judgment quality is _greater_ when we say someone is a criminal than when we say someone is innocent.

What about the criminals who walked?
Surely they should be accounted for.
Enter recall.

# Recall
> ... and recall as a measure of quantity.

Recall is algebraically defined as:

$$
Recall = \frac{TP}{TP + FN}
$$

We can have high-quality judgment, but it doesn't mean we do it often.
Similar to precision, we calculate recall from both sides.
One for the criminal:

$$
\begin{align}
Precision_{criminal} & = \frac{47}{47 + 3} \\\\
& = \frac{47}{50} \\\\
& = 0.94
\end{align}
$$

And one for the innocent:

$$
\begin{align}
Precision_{innocent} & = \frac{48}{48 + 2} \\\\
& = \frac{48}{50} \\\\
& = 0.96
\end{align}
$$

These values look similar to the precision values (more on that in a bit), but reversed.
The recall when convicting someone as a criminal is 0.94 and 0.96 when judging someone as innocent.
Combining this with precision, we could say that our quality of convicting criminals is good, but we let a few get away.
Likewise, our quality of judging someone as innocent isn't as great, but we tend to say more people are innocent.
As a result, we correctly label more innocent people.
Maybe you could say we're a "soft" judge.

# Imbalanced 🙃
Why do the values for precision and recall look so similar?
Because the true labels of the classes are balanced and, while not perfect, our judgment was fairly balanced
(51 innocents vs 49 criminals).