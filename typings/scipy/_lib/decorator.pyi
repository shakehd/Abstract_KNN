from _typeshed import Incomplete
from contextlib import GeneratorContextManager as _GeneratorContextManager
from typing import NamedTuple

__version__: str

def get_init(cls): ...

class ArgSpec(NamedTuple):
    args: Incomplete
    varargs: Incomplete
    varkw: Incomplete
    defaults: Incomplete

def getargspec(f): ...

DEF: Incomplete

class FunctionMaker:
    shortsignature: Incomplete
    name: Incomplete
    doc: Incomplete
    module: Incomplete
    annotations: Incomplete
    signature: Incomplete
    dict: Incomplete
    defaults: Incomplete
    def __init__(self, func: Incomplete | None = ..., name: Incomplete | None = ..., signature: Incomplete | None = ..., defaults: Incomplete | None = ..., doc: Incomplete | None = ..., module: Incomplete | None = ..., funcdict: Incomplete | None = ...) -> None: ...
    def update(self, func, **kw) -> None: ...
    def make(self, src_templ, evaldict: Incomplete | None = ..., addsource: bool = ..., **attrs): ...
    @classmethod
    def create(cls, obj, body, evaldict, defaults: Incomplete | None = ..., doc: Incomplete | None = ..., module: Incomplete | None = ..., addsource: bool = ..., **attrs): ...

def decorate(func, caller): ...
def decorator(caller, _func: Incomplete | None = ...): ...

class ContextManager(_GeneratorContextManager):
    def __call__(self, func): ...

init: Incomplete
n_args: Incomplete

def __init__(self, g, *a, **k) -> None: ...

contextmanager: Incomplete

def append(a, vancestors) -> None: ...
def dispatch_on(*dispatch_args): ...
