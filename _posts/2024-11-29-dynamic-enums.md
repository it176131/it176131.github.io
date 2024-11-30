---
layout: "post"
title: "Dynamic Enums"
date: 2024-11-29
---

My go-to choice for validating JSON files is [`pydantic`](https://docs.pydantic.dev/latest/).
It's fast, reliable, and relatively flexible.

A feature I really appreciate is the ability to validate a field value against an [`Enum`](https://docs.python.org/3/library/enum.html).
Here's the example from the [`pydantic` `Enum` docs](https://docs.pydantic.dev/latest/api/standard_library_types/#enum):
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
