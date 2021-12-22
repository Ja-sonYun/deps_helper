# dependency helper

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/deps-helper/0.1.3)](https://pypi.org/project/deps-helper/) [![PyPI version](https://badge.fury.io/py/deps-helper.svg)](https://badge.fury.io/py/deps-helper)

Dependency helper for properties of python class

```$ pip install deps_helper```

```python
from deps_helper import Dependencies


new_Dep = Dependencies.new("A")

class A(new_Dep):
    #  "_for" can be an array
    @new_Dep.register(_for="first_operation")[int]  # support type hinting, tested in pyright
    def number(self, value):
        return value

    @new_Dep.guard()
    def first_operation(self):
        ...


>>> a = A()
>>> a.first_operation()
Traceback (most recent call last):
...
AttributeError: ("follow attributes are not assigned for first_operation => ", [number])
>>> a.number = 2
>>> a.first_operation()  # OK
>>>
```
