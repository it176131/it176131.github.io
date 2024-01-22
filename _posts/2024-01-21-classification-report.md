---
layout: "post"
title: "Classification Report"
date: 2024-01-21
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

In a meeting last week, I heard someone say, "We achieved a classification score of 99%."
He was referring to accuracy.
And to the untrained ear this may sound impressive, but not to me.

# Accuracy
The data in this particular problem is what we call "imbalanced."
If it were balanced or approximately balanced, I wouldn't have thought too much about the score.
Why?
Let me highlight the issue with an example.

Suppose you're taking a test with 10 True or False questions.
The number of actual True and False answers is five and five.
You take the test and get eight out ten correct.
Your accuracy is 80%.<br><br>

$$
\begin{align}
Accuracy = \frac{Number\ correct}{Total}
\end{align}
$$

<br>
Now suppose you take another test.
This test also has 10 True or False questions, but only two of them are actually False.
You get eight of ten correct again.
Should we consider the two test scores equal?
Mathematically, yes, but the quality of tester could be considered vastly different.

# Confusion matrix
This is a classic binary classification problem.
We can look at the answers and differentiate _how_ we were correct or incorrect using a
[confusion matrix](https://en.wikipedia.org/wiki/Confusion_matrix).

|                     |      Actual True      |     Actual False      |
|:-------------------:|:---------------------:|:---------------------:|
| **Predicted True**  | True Positive ($TP$)  | False Positive ($FP$) |
| **Predicted False** | False Negative ($FN$) | True Negative ($TN$)  |

**True Positives** and **True Negatives** are the values we labeled correctly.
**False Positives** are a [type I error](https://en.wikipedia.org/wiki/Type_I_and_type_II_errors#Type_I_error)—
we incorrectly said True when it was False.
**False Negatives** are a [type II error](https://en.wikipedia.org/wiki/Type_I_and_type_II_errors#Type_II_error)—
we incorrectly said False when it was True.
We define accuracy algebraically using all four:<br><br>

$$
Accuracy = \frac{TP + TN}{TP + FP + TN + FN}
$$

<br>
In the first test, our confusion matrix could look like this:

|                     | Actual True | Actual False |
|:-------------------:|:-----------:|:------------:|
| **Predicted True**  |      4      |      1       |
| **Predicted False** |      1      |      4       |

Or maybe like this:

|                     | Actual True | Actual False |
|:-------------------:|:-----------:|:------------:|
| **Predicted True**  |      5      |      2       |
| **Predicted False** |      0      |      3       |

Either way, our accuracy is 80%.
To numerically understand the difference, we rely on two other metrics,
[precision and recall](https://en.wikipedia.org/wiki/Precision_and_recall).

# Precision
> Precision can be seen as a measure of quality, ...

<br>

$$
Precision = \frac{TP}{TP + FP}
$$

<br>
Because we have two ways of answering a question (True or False),
we must calculate precision from both sides:
- Where True is the positive and False is the negative,
- and where False is the positive and True is the negative.

We'll do this for both tests.

|                     |               Test #1               |               Test #2                |
|:-------------------:|:-----------------------------------:|:------------------------------------:|
| $Precision_{True}$  | $\frac{4}{4+1} = \frac{4}{5} = 0.8$ | $\frac{5}{5+2} = \frac{5}{7} = 0.71$ |
| $Precision_{False}$ | $\frac{4}{4+1} = \frac{4}{5} = 0.8$ | $\frac{3}{3+0} = \frac{3}{3} = 1.00$ |

For test #1, our "quality" of correctly marking a question True or False is equal at 0.80.
For test #2, our quality is maxed out when marking a question False i.e.,
when we say False, we get it right 100% of the time.
But when we mark a question as True, our quality falls.
We're not as good at correctly guessing True compared to False.

# Recall
> ... and recall as a measure of quantity.

<br>

$$
Recall = \frac{TP}{TP + FN}
$$

<br>
Having high precision ("quality") doesn't mean that we correctly label _all_ of the questions in a given category.
Recall can show us that we miss some.

|                  |               Test #1               |               Test #2                |
|:----------------:|:-----------------------------------:|:------------------------------------:|
| $Recall_{True}$  | $\frac{4}{4+1} = \frac{4}{5} = 0.8$ | $\frac{5}{5+0} = \frac{5}{5} = 1.00$ |
| $Recall_{False}$ | $\frac{4}{4+1} = \frac{4}{5} = 0.8$ | $\frac{3}{3+2} = \frac{3}{5} = 0.60$ |

The recall results for test #1 are the same as precision.
This is because the balance of our correct to incorrect answers is split evenly between the classes.
The recall for test #2, however, is a bit different.
When we marked an answer as True, our recall is 1.00.
You could say that we tend to mark more answers as True and therefore capture a higher quantity of the
(correct and incorrect) answers.
On the False side, our recall is 0.60.
While our quality in determining an answer as False is outstanding, we don't mark enough answers as False.
Our quantity is low.

# F1 score

$$
\begin{align}
F1 & = (\frac{precision^{-1} + recall^{-1}}{2})^{-1} \\\\
& = 2\times\frac{precision \times recall}{precision + recall}
\end{align}
$$

<br>
Precision and recall together give us a better idea of how we performed on the test.
But looking at four numbers (or more when greater than two classes) can be a tad overwhelming.
We can make it easier by calculating the F1 score—
the [harmonic mean](https://en.wikipedia.org/wiki/Harmonic_mean) of precision and recall.

|              |                                    Test #1                                    |                                       Test #2                                       |
|:------------:|:-----------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|
| $F1_{True}$  | $2 \times \frac{0.8 \times 0.8}{0.8 + 0.8} = 2 \times \frac{0.64}{1.6} = 0.8$ | $2 \times \frac{0.71 \times 1.00}{0.71 + 1.00} = 2 \times \frac{0.71}{1.71} = 0.83$ |
| $F1_{False}$ | $2 \times \frac{0.8 \times 0.8}{0.8 + 0.8} = 2 \times \frac{0.64}{1.6} = 0.8$ | $2 \times \frac{1.00 \times 0.60}{1.00 + 0.60} = 2 \times \frac{0.60}{1.60} = 0.75$ |

# Imbalanced 🙃
The F1 scores look pretty close to the accuracy; how do all these metrics help us with an imbalanced data set?
Let's explore an example.
We work in radiology and are trying to detect breast cancer through imaging.
Breast cancer is somewhat rare; [one in eight average women will develop it.](https://www.cancer.org/cancer/types/breast-cancer/about/how-common-is-breast-cancer.html)
That's 13%.
If we looked at every image and said "no cancer", we'd be correct 87% of the time.
That's a pretty high accuracy!
But it's not the right metric.
With this method, we'd miss 100% of all cancer patients.
To improve, perhaps we should focus on precision instead.

Here are two classification reports for 100 potential cancer patients.
Can you tell which one performed better?
Note that "support" is the number of observations in a given class (cancer vs no cancer).

Report #1

|           | precision | recall | f1-score | support |
|-----------|-----------|--------|----------|---------|
| cancer    | NaN       | 0.00   | NaN      | 13      |
| no cancer | 0.87      | 1.00   | 0.93     | 87      |
|           |           |        |          |         |
| accuracy  |           |        | 0.87     | 100     |

Report #2

|           | precision | recall | f1-score | support |
|-----------|-----------|--------|----------|---------|
| cancer    | 0.38      | 0.23   | 0.29     | 13      |
| no cancer | 0.89      | 0.94   | 0.92     | 87      |
|           |           |        |          |         |
| accuracy  |           |        | 0.85     | 100     |

If we care about successfully detecting breast cancer and potentially saving a life,
then the second model performed significantly better.
While the first model did classify more patients correctly, it completely missed all signs of cancer.
The second model did mislabel some patients as having cancer, which has its own cost ramifications,
but it may be better to be safe than sorry.

Next time you hear someone say their model achieved 99% accuracy, ask them for a classification report.

<script src="https://giscus.app/client.js"
        data-repo="it176131/it176131.github.io"
        data-repo-id="R_kgDOK1ukqg"
        data-category="Announcements"
        data-category-id="DIC_kwDOK1ukqs4CcOnS"
        data-mapping="pathname"
        data-strict="0"
        data-reactions-enabled="1"
        data-emit-metadata="0"
        data-input-position="top"
        data-theme="light"
        data-lang="en"
        data-loading="lazy"
        crossorigin="anonymous"
        async>
</script>