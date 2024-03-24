---
layout: "post"
title: "Contributing, Part II: Unit Tests"
date: 2024-03-24
---

Throughout my professional career I've picked up a few skills.
One of the more recent ones is called
[_test-driven development_](https://en.wikipedia.org/wiki/Test-driven_development).

Most of my code writing experience has included scripting, analysis and modeling in notebooks,
and some local package development.
I'd never successfully written a unit test, nor did I really understand what they were for.
In my new role, I experienced baptism by fire and was introduced to a more mature form of software development.

# A Not So Great Example
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

# Test-Driven Development
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
The good news is that the
[existing unit tests for `TransactionEncoder`](https://github.com/rasbt/mlxtend/blob/master/mlxtend/preprocessing/tests/test_transactionencoder.py)
are easy to find!

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