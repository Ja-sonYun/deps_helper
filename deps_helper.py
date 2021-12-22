import functools
from types import new_class
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast, Generic


class NotAssigned:
    e = None


T = TypeVar("T")
G = TypeVar("G")
MayAssigned = Union[Type[NotAssigned], T]


def unwrap_assigned(may_assigned: MayAssigned[T]) -> T:
    assert may_assigned is not NotAssigned
    return cast(T, may_assigned)


class RegDependencyBase(Generic[G]):
    __mapper = "_mapper"

    def __init__(self, func: Callable[[Any, G], Optional[Any]]):
        self.func = func
        self.attr_name = func.__name__
        self.last_value: MayAssigned[G] = NotAssigned

        # register new attribute name into mapper
        getattr(self, RegDependencyBase.__mapper)(self.attr_name)

    def __get__(self, *_) -> G:
        if self.last_value is NotAssigned:
            raise AttributeError(f"'{self.attr_name}' is not assigned")

        return unwrap_assigned(self.last_value)

    def __set__(self, instance: "Dependencies", value: G):
        last_value = self.func(instance, value)
        if last_value is None:
            self.last_value = value
        else:
            self.last_value = last_value

    @staticmethod
    def _append_mapper(
        mapper: dict, _for: Union[List[str], str]
    ) -> Callable[[Type["RegDependencyBase"], str], None]:
        all_deps = [_for] if isinstance(_for, str) else _for

        def attr_mapper(_, attr_name: str):
            for _for in all_deps:
                if _for in mapper:
                    mapper[_for].append(attr_name)
                else:
                    mapper[_for] = [attr_name]

        return attr_mapper

    @staticmethod
    def _create_with_for(
        _for: Union[List[str], str], _dependency_map: dict[str, List[str]]
    ) -> Type["RegDependencyBase"]:
        def adder(ns: dict[str, Any]) -> None:
            ns[RegDependencyBase.__mapper] = RegDependencyBase._append_mapper(
                _dependency_map, _for
            )

        return cast(
            Type[RegDependencyBase],
            new_class("RegDependency", (RegDependencyBase, Generic[G]), None, adder),
        )


class RegReqMeta(type):
    key = "__registered_attr__"

    def __new__(cls, name, bases, dct):
        dct[RegReqMeta.key] = []
        for _, v in dct.items():
            if isinstance(v, RegDependencyBase):
                dct[RegReqMeta.key].append(v.attr_name)

        return super().__new__(cls, name, bases, dct)


class Dependencies(metaclass=RegReqMeta):
    __dep_mapper_key__ = "__dependency_map__"
    _register = RegDependencyBase

    @staticmethod
    def get_dependency_map(_=None) -> dict[str, List[str]]:
        # dummy function for type checking. This will be implmented in new()
        # dummy underscore for make this accessable from not only staticmethod
        ...

    @staticmethod
    def new(name: str) -> Type["Dependencies"]:
        def adder(ns: dict[str, Any]) -> None:
            ns[Dependencies.__dep_mapper_key__] = {}

        new_deps_obj = cast(
            Type[Dependencies],
            new_class("Dependencies_" + name, (Dependencies,), None, adder),
        )

        new_deps_obj.get_dependency_map = lambda _=None: getattr(
            new_deps_obj, Dependencies.__dep_mapper_key__
        )

        return new_deps_obj

    @classmethod
    def register(cls, *, _for: Union[str, List[str]] = "*"):
        new_dep = RegDependencyBase._create_with_for(_for, cls.get_dependency_map())
        return new_dep

    @classmethod
    def guard(
        cls, *, _for: Optional[str] = None, cb=Optional[Callable], _raise: bool = True
    ) -> Callable:
        def guarder(func):
            _for_ = _for if _for is not None else func.__name__

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                self = args[0]
                if self.check_dependencies(_for=_for_, _raise=_raise):
                    return cb()
                return func(*args, **kwargs)

            return wrapper

        return guarder

    def check_dependencies(self, *, _for: str = "*", _raise: bool = True) -> List[str]:
        not_assigned = []

        if _for == "*":
            for attr in getattr(self, RegReqMeta.key):
                try:
                    getattr(self, attr)
                except AttributeError:
                    not_assigned.append(attr)

            if not_assigned and _raise:
                raise AttributeError(
                    f"follow attributes are not assigned for '{_for}' => ", not_assigned
                )

        elif _for in self.get_dependency_map():
            for dep in self.get_dependency_map()[_for]:
                try:
                    getattr(self, dep)
                except AttributeError:
                    not_assigned.append(dep)

            if not_assigned and _raise:
                raise AttributeError(
                    f"follow attributes are not assigned => ", not_assigned
                )
        else:
            raise ValueError(f"No dependencies for '{_for}'")

        return not_assigned


if __name__ == "__main__":
    a_dep = Dependencies.new("A")

    def raiseerr():
        print("faisdkljaslkdjeld")

    class A(a_dep):
        @a_dep.register(_for="aa")[int]
        def a(self, value):
            return value

        @a_dep.register(_for=["bb", "aa"])[int]
        def b(self, value):
            return str(value)

        @a_dep.guard()
        def aa(self):
            print("all good")

        @a_dep.guard()
        def bb(self):
            print("all good")

    def wwww(we: int):
        print(we)

    w = A()
    w.a = 2
    print(w.a)
    #  w.b = wwww
    w.aa()
    w.bb()
