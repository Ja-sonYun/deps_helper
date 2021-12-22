# dependency helper
Dependency helper for properties of python class

```python
new_Dep = Dependencies.new("A")

class A(new_Dep):
    #  "_for" can be an array
    @new_Dep.register(_for="first_operation")[int]  # support type hinting, tested in pyright
    def number(self, value):
        return value
        
    @new_Dep.guard()
    def first_operation():
        ...
        
        
>>> a = A()
>>> a.first_operation() 
Traceback (most recent call last):
...
AttributeError: ("follow attributes are not assigned for first_operation => ", [number])

>>> a.number = 2
>>> a.first_operation()
>>>
        
 
```
