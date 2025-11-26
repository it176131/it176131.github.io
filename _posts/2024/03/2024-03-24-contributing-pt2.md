---
layout: "post"
title: "Contributing, Part II: Test-Driven Development"
date: 2024-03-24
images: "/assets/images/2024-03-24-contributing-pt2"
---

Throughout my professional career I've picked up a few skills.
One of the more recent ones is called
[_test-driven development_](https://en.wikipedia.org/wiki/Test-driven_development).

Most of my code writing experience has included scripting, analysis and modeling in notebooks,
and some local package development.
I'd never successfully written a unit test, nor did I really understand what they were for.
In my new role, I experienced baptism by fire and was introduced to a more mature form of software development.

# A Not-So-Great Example
I first discovered unit tests while studying 
[object-oriented programming](https://en.wikipedia.org/wiki/Object-oriented_programming).
The videos and articles would give toy examples that seemed easy to comprehend,
but I couldn't figure out why you'd want to write them in the first place.
I remember one example where the function being tested was to add two values and return the result.

```python
def add(a, b):
    return a + b

```

The following may have been an example unit test.

```python
def test_add():
    a, b = 1, 2
    expected = 3
    actual = add(a=a, b=b)
    assert actual == expected

```

While this unit test is valid, it doesn't highlight the power and importance of unit testing your code.

# Test First, Develop Second
My memory may be failing me here,
but I don't think introducing a function _and then_ a corresponding unit test is the best way to teach unit tests.
In test-driven development (TDD),
you design a test to check if a function returns an expected output given an input _before_ you write the function.
This means the test _should_ fail right off the bat.
Your mission, should you choose to accept it,
is to develop the function that allows the unit test to pass... 
without causing any other previously passing tests to fail.

# A Better Example
As of 2024-03-24, my [request](https://github.com/rasbt/mlxtend/issues/1085)
to add the `get_feature_names_out` method to `mlxtend`'s `TransactionEncoder` class was 
[approved](https://github.com/rasbt/mlxtend/issues/1085#issuecomment-2016839528).
This is a real-world scenario where TDD can help keep the PR in scope, resulting in an easier merge.

To kick things off, I
[forked](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/fork-a-repo)
the `mlxtend` repo.
This allows me to develop on a copy of the repo before submitting a
[pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)
(PR) to the original repo.
I then cloned the forked repo to my machine, created a virtual environment, and installed the
[requirements.txt](https://github.com/rasbt/mlxtend/blob/master/requirements.txt) and `mlxtend` package from the source.

> How I installed the requirements.txt.
> ```shell
> pip install -r requirements.txt
> ```

> How I installed `mlxtend` from the source.
> ```shell
> pip install -e .
> ```

After installation, I looked for the unit tests.
Every package has its quirks and `mlxtend` is no different—the package doesn't use python's built-in
[`unittest`](https://docs.python.org/3/library/unittest.html) nor the third party
[`pytest`](https://docs.pytest.org/en/8.0.x/) (my preferred testing framework).
The author appears to have written his own testing functions,
e.g. [`assert_raises`](https://rasbt.github.io/mlxtend/api_modules/mlxtend.utils/assert_raises/),
and rather than put all tests in a single, dedicated directory, he chose to put them with their respective packages.
I won't fault him for it as it's a valid design approach, though not one I encounter very often.
The good news is that the existing
[unit tests](https://github.com/rasbt/mlxtend/blob/master/mlxtend/preprocessing/tests/test_transactionencoder.py)
for `TransactionEncoder` are easy to find!

# Preexisting Tests
It's typically good practice to run all the preexisting unit tests _before_ making changes.
This helps ensure that we're starting with a functioning code base.
To do this, I tried running a single test in
[PyCharm](https://www.jetbrains.com/pycharm/)
(my preferred [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment))
by clicking the green "play" button ▶️ next to a test.

![Preexisting Unit Test]({{ page.images | relative_url }}/preexisting_unit_test.png)

Rather than a test passing, I was greeted with an error:

```text
ModuleNotFoundError: No module named 'pytest'
```

Well that's confusing 😕.
Pytest wasn't listed in the requirements.txt file, so I didn't install it.

After some tinkering, I installed Pytest and the test I had tried to run previously ran and passed.
This had me curious, so I searched "pytest" in the repo.
Turns out I somehow missed the
[CONTRIBUTING.md](https://github.com/rasbt/mlxtend/blob/master/docs/sources/CONTRIBUTING.md)
file which explicitly says to use pytest.
How'd I miss that 🤦.

To ensure that I didn't miss any other packages, I checked through the
[environment.yml](https://github.com/rasbt/mlxtend/blob/b3b81f4dd603e0ad9c8f3133f1b2bf2f5177cc9d/environment.yml)
file and found some discrepancies between it and the requirements.txt.
Maybe I'll log another issue after this one to update the requirements.txt.
Or maybe you'll do it, and we can be co-contributors 😉.

Moving on (and following the CONTRIBUTING.md guide), I ran all unit tests with the following command:

```shell
PYTHONPATH='.' pytest ./mlxtend -sv
```

Surprisingly (or maybe unsurprisingly at this point), 20 tests failed out of 694 total ran.
Drilling down to the test_transactionencoder.py file, one out of six tests failed.
It's important to remember that my commits and PR should only handle what's in the scope of the feature request.
Anything more and this can very quickly turn into a mess that's difficult to merge.
With that, I created a branch and added some new tests to help guide my test-driven development.

# New Branch, New Tests
Normally when I create a branch I try to name it according to what's on it.
In this case I chose to name it "issue_1085" since my feature request has URL
[https://github.com/rasbt/mlxtend/issues/1085](https://github.com/rasbt/mlxtend/issues/1085).

```shell
git checkout -b issue_1085
```

From here I was free to write and commit code.

In true TDD fashion, [I added two tests to the tests/test_transactionencoder.py file first](https://github.com/rasbt/mlxtend/pull/1087/commits/45cb6cd5d86fcd037107e318225d722bd98d5668).

```python
def test_get_feature_names_out():
    """Assert TransactionEncoder has attribute get_feature_names_out."""
    oht = TransactionEncoder()
    assert hasattr(oht, "get_feature_names_out")


def test_set_output():
    """Assert TransactionEncoder has attribute set_output."""
    oht = TransactionEncoder()
    assert hasattr(oht, "set_output")

```

Both of these immediately failed.
To make them pass [I added the `get_feature_names_out` method to the `TransactionEncoder` in transactionencoder.py file](https://github.com/rasbt/mlxtend/pull/1087/commits/943457534788862512cc6d28d41963019b23c4b5).

```python
class TransactionEncoder(BaseEstimator, TransformerMixin):
    
    ...
    
    def get_feature_names_out(self, input_features=None):
        """Used to get the column names of pandas output.
        
        This method combined with the TransformerMixin exposes the
        set_output API to the TransactionEncoder. This allows the user
        to set the transformed output to a pandas.DataFrame by default.
        See  https://scikit-learn.org/stable/developers/develop.html#developer-api-set-output
        for more details.
        """
        ...

```

This exposed the `set_output` method, resulting in both tests passing.
I then needed to check that the `set_output` and `get_feature_names` methods actually worked,
so [I updated the tests into a failing state again](https://github.com/rasbt/mlxtend/pull/1087/commits/b21bb21e8461225f455e8ea19c5f9cb948e16f29).

```python
import pandas as pd

...

def test_get_feature_names_out():
    """Assert TransactionEncoder has attribute get_feature_names_out."""
    oht = TransactionEncoder()
    assert hasattr(oht, "get_feature_names_out")
    oht.fit(dataset)
    np.testing.assert_array_equal(oht.get_feature_names_out(), oht.columns_)


def test_set_output():
    """Assert TransactionEncoder has attribute set_output.
    
    When transform="pandas", the transformed output of
    TransactionEncoder should be a pandas.DataFrame with the correct
    column names and the values should match those of the original
    numpy.array.
    """
    oht = TransactionEncoder()
    assert hasattr(oht, "set_output")
    oht = oht.set_output(transform="pandas")
    out = oht.fit_transform(dataset)
    assert isinstance(out, pd.DataFrame)
    np.testing.assert_array_equal(out.columns, oht.columns_)

```

Amazingly enough, the only part of the tests that failed was when I checked if the columns aligned.
The `set_output` wrapper handled everything else automatically 🚀.

To get back to a passing state, [I had to modify the `get_feature_names_out` method](https://github.com/rasbt/mlxtend/pull/1087/commits/0167c8f59a890982bfbfa88352cb0ac3875a8bd9).
I wanted to get an idea of what it should look like,
so I took a peak at `scikit-learn`'s [`OneToOneFeatureMixin`](https://scikit-learn.org/stable/modules/generated/sklearn.base.OneToOneFeatureMixin.html) and [`ClassNamePrefixFeaturesOutMixin`](https://scikit-learn.org/stable/modules/generated/sklearn.base.ClassNamePrefixFeaturesOutMixin.html)
and used their implementations as a template.

```python
from sklearn.utils.validation import check_is_fitted, _check_feature_names_in

...

class TransactionEncoder(BaseEstimator, TransformerMixin):

    ...
    
    def get_feature_names_out(self):
        """Used to get the column names of pandas output.

        This method combined with the TransformerMixin exposes the
        set_output API to the TransactionEncoder. This allows the user
        to set the transformed output to a pandas.DataFrame by default.

        See  https://scikit-learn.org/stable/developers/develop.html#developer-api-set-output
        for more details.
        """
        check_is_fitted(self, attributes="columns_")
        return _check_feature_names_in(estimator=self, input_features=self.columns_)

```

And with that, the unit tests passed and the `set_output` method had been successfully integrated!

# Pull Request
Just before pushing my code and opening a pull request to merge everything,
I took one final look at the CONTRIBUTING.md file.
I had checked off most of the boxes under [Quick Contributor Checklist](https://github.com/rasbt/mlxtend/blob/master/docs/sources/CONTRIBUTING.md#quick-contributor-checklist), but forgot two:
- Modify documentation in the appropriate location under `mlxtend/docs/sources/`
- Add a note about the modification/contribution to the `./docs/sources/changelog.md` file

Because my feature is so small, the work to update the user guide and changelog was relatively light.
The hardest part was figuring out how to word everything and then link to a PR that didn't exist yet.
In the end it came out looking alright.
I pushed my code to my forked repo and opened a pull request.
Now I wait for feedback from the author and any other contributors.
[Following along here!](https://github.com/rasbt/mlxtend/pull/1087)