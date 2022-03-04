# dependency helper

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/deps-helper/0.1.3)](https://pypi.org/project/rich/) [![PyPI version](https://badge.fury.io/py/deps-helper.svg)](https://badge.fury.io/py/deps-helper)

Dependency helper for properties of python class

```$ pip install deps_helper```

```python
from deps_helper import Dependencies


class A(deps := Dependencies.new()):
    #  "_for" can be an array
    @deps.register(_for="operation")
    def requested_by(self, user):
        print(f"operation requested by {user}.")

        return user

    @deps.guard()
    def operation(self):
        ...



>>> a = A()
>>> a.operation()
Traceback (most recent call last):
...
AttributeError: ("follow attributes are not assigned for operation => ", [requested_by])
>>> a.requested_by = "admin"
operation requested by admin.
>>> a.operation()  # OK
>>>
```
