---
layout: "post"
title: "Dynamic Enums"
date: 2024-11-29
---

My go-to choice for validating [JSON](https://www.json.org/json-en.html) files is [`pydantic`](https://docs.pydantic.dev/latest/).
It's fast, reliable, and relatively flexible.

A feature I really appreciate is the ability to validate a field value against an [`Enum`](https://docs.python.org/3/library/enum.html).
Here's the example from the [`pydantic` v2.10 `Enum` docs](https://docs.pydantic.dev/2.10/api/standard_library_types/#enum):
```python
from enum import Enum, IntEnum

from pydantic import BaseModel, ValidationError


class FruitEnum(str, Enum):
    pear = "pear"
    banana = "banana"


class ToolEnum(IntEnum):
    spanner = 1
    wrench = 2


class CookingModel(BaseModel):
    fruit: FruitEnum = FruitEnum.pear
    tool: ToolEnum = ToolEnum.spanner


print(CookingModel())
#> fruit=<FruitEnum.pear: 'pear'> tool=<ToolEnum.spanner: 1>
print(CookingModel(tool=2, fruit="banana"))
#> fruit=<FruitEnum.banana: 'banana'> tool=<ToolEnum.wrench: 2>
try:
    CookingModel(fruit="other")
except ValidationError as e:
    print(e)
    """
    1 validation error for CookingModel
    fruit
      Input should be 'pear' or 'banana' [type=enum, input_value='other', input_type=str]
    """
```

>[!NOTE]
>
>[`mypy`](https://mypyc.readthedocs.io/en/latest/index.html), another tool I've grown to love, would raise [`[arg-type]` errors](https://mypy.readthedocs.io/en/stable/error_code_list.html#check-argument-types-arg-type) on these lines:
>```python
>...
>print(CookingModel(tool=2, fruit="banana"))  # [arg-type] error
>...
>CookingModel(fruit="other")  # [arg-type] error
>```

# The Problem
Defining an `enum` is great when you only have a handful of valid values,
but what if you have more?
And I don't mean like 10 or 20—I mean something closer to 50.

Typing out all the values into the `enum` class is a valid approach, but that can lead to mistakes (and I'm lazy).
A much better approach would be to have someone else type out all the values. 😂

No, really.
I'm serious.
My job isn't to come up with the values in the JSON files, but to validate them.
Which means someone else has already come up with a list of 50 _valid_ values.
And lucky for me, I have that list in a [YAML](https://yaml.org/) file.

# The Solution
Before I can construct an `enum` out of the values in the YAML file, I'll need to extract them.
I can do this with the [`PyYAML`](https://pyyaml.org/) package.
```yaml
# The yaml file contents.
us_states: [AL, AK, AZ, AR, CA, CO, CT, DE, FL, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY]
```
```python
"""Contents of main.py"""

from yaml import load, Loader


def _get_valid_values() -> list[str]:
    """Read the yaml file and return a list of valid values."""
    with open("valid_values.yaml", mode="rb") as yml_file:
        data = load(stream=yml_file, Loader=Loader)

    valid_values: list[str] = data["us_states"]
    return valid_values


if __name__ == "__main__":
    valid_values = _get_valid_values()
    print(len(valid_values))  # 50

```

Once we have the values as a `Python` object,
we need to [subclass `enum.Enum`](https://docs.python.org/3/howto/enum.html) and assign them.
But how?
On first attempt, maybe we call the `_get_valid_values` function within our new `enum` class:
```python
"""Contents of main.py"""

from enum import Enum

from yaml import load, Loader


def _get_valid_values() -> list[str]: ...


class State(str, Enum):
    """Enumerations of valid values."""
    
    _get_valid_values()


if __name__ == "__main__":
    try:
        print(repr(State(value="MO")))
    except Exception as exc:
        print(repr(exc))

```
But this raises the following `TypeError`:
>TypeError("<enum 'State'> has no members; specify `names=()` if you meant to create a new, empty, enum")

No, we can't just call `_get_valid_values` and expect the values to be assigned in the `State` enum.
Or can we?
```python
"""Contents of main.py"""

from enum import Enum

from yaml import load, Loader


def _get_valid_values() -> list[str]: ...


class State(str, Enum):
    """Enumerations of valid values."""
    
    # https://docs.python.org/3/library/enum.html#enum.Enum._ignore_
    _ignore_ = ["State", "value"]
    State = vars()
    for value in _get_valid_values():
        State[value] = value


if __name__ == "__main__":
    try:
        print(repr(State(value="MO")))  # <State.MO: 'MO'>
    except Exception as exc:
        print(repr(exc))

```
It turns out
that you _can_ assign the values within the `enum`
by using the private [`_ignore_`](https://docs.python.org/3/library/enum.html#enum.Enum._ignore_) value.
From the [docs](https://docs.python.org/3/library/enum.html#enum.Enum._ignore_):
>`_ignore_` is a list of names that will not become members,
> and whose names will also be removed from the completed enumeration.
> See [TimePeriod](https://docs.python.org/3/howto/enum.html#enum-time-period) for an example.

To be more specific,
assigning `_ignore_` to `["State", "value"]` means we can use `State` and `value` as variables within the class's logic.
Not ignoring "value" would result in a `TypeError` saying we've already assigned `value`,
and not ignoring "State" would assign `State` as a valid value (which we don't want).

From here we can validate our JSON by adding `State` to a `pydantic` model.
No more manually updating our `State` `enum`.
```python
"""Contents of main.py"""

from enum import Enum
import json

from pydantic.main import BaseModel
from yaml import load, Loader


def _get_valid_values() -> list[str]: ...


class State(str, Enum): ...


class Location(BaseModel):
    state: State


if __name__ == "__main__":
    some_json_string = '{"state": "MO"}'
    data = json.loads(s=some_json_string)
    try:
        print(repr(Location(**data)))  # Location(state=<State.MO: 'MO'>)
    except Exception as exc:
        print(repr(exc))

```

# Bonus
While poking around the web for other ways to dynamically create `enum`s,
I found [this post on dev.to](https://dev.to/ivergara/dynamic-generation-of-informative-enum-s-in-python-1b22)
```python
"""Contents of main.py"""

from enum import Enum
import json

from pydantic.main import BaseModel
from yaml import load, Loader


def _get_valid_values() -> list[str]: ...


State = Enum(value="State", names={v: v for v in _get_valid_values()})


class Location(BaseModel):
    state: State


if __name__ == "__main__":
    some_json_string = '{"state": "MO"}'
    data = json.loads(s=some_json_string)
    try:
        print(repr(Location(**data)))  # Location(state=<State.MO: 'MO'>)
    except Exception as exc:
        print(repr(exc))

```

I like this solution because of its simplicity, but `mypy` raises a [`[misc]` error](https://mypy.readthedocs.io/en/stable/error_code_list.html#miscellaneous-checks-misc) saying:
>Second argument of Enum() must be string, tuple, list or dict literal for mypy to determine Enum members

Because of this, I will be sticking with my inheritance approach.