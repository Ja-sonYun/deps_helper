# dependency helper

[![Supported Python Versions](https://img.shields.io/pypi/pyversions/deps-helper/0.1.6)](https://pypi.org/project/deps-helper/) [![PyPI version](https://badge.fury.io/py/deps-helper.svg)](https://badge.fury.io/py/deps-helper)

Dependency helper for properties of python class

```$ pip install deps_helper```

```python
from deps_helper import Dependencies


class A(deps := Dependencies.new()):
    @deps.register(_for="operation")
    def requested_by(self, user):
        print(f"operation requested by {user}.")

        return f"requested by {user}"

    @deps.register(_for=["check_validity", "operation"])
    def validity(*_):
        ...

    @deps.guard()
    def operation(self):
        print("execute operation...")

    @deps.guard()
    def check_validity(self):
        if self.validity:
            print("Ok")


>>> a = A()
>>> a.check_validity()
Traceback (most recent call last):
...
AttributeError: ("follow attributes are not assigned for check_validity => ", [validity])
>>> a.operation()
Traceback (most recent call last):
...
AttributeError: ("follow attributes are not assigned for operation => ", [requested_by, validity])
>>> a.validity = True
>>> a.check_validity()
Ok
>>> a.requested_by = "admin"
operation requested by admin.
>>> a.operation()
execute operation...
>>> print(a.requested_by)
requested by admin
>>>
```
