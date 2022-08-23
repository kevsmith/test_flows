from functools import wraps
import json

class MatchExpr:

    def __init__(self, **kwargs):
        self._match = {}
        for key in kwargs.keys():
            self._match[key] = kwargs[key]

    def __str__(self):
        entries = []
        for key in self._match:
            value = self._match[key]
            entries.append(f"{key} == {value}")
        return " ".join(entries)

class OrExpr:

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __str__(self):
        return f"{str(self._left)} or {str(self._right)}"

class AndExpr:

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def __str__(self):
        return f"{str(self._left)} and {str(self._right)}"

class Matcher:

    def __init__(self, **kwargs):
        self._expr = MatchExpr(**kwargs)

    def or_(self, **kwargs):
        if self._expr is None:
            self._expr = MatchExpr(**kwargs)
        else:
            self._expr = OrExpr(self._expr, MatchExpr(**kwargs))
        return self
    
    def and_(self, **kwargs):
        if self._expr is None:
            self._expr = MatchExpr(**kwargs)
        else:
            self._expr = AndExpr(self._expr, MatchExpr(**kwargs))
        return self

    def __str__(self):
        return f"match_on: {str(self._expr)}"

    def __call__(self, *args, **kwargs):
        wrapped = args[0]
        if hasattr(wrapped, "_match_on") == False:
            wrapped._match_on = str(self._expr)
        return wrapped

def trigger_when(*args, **kwargs):
    return Matcher(**kwargs)

@trigger_when(event_name="mf.simple_flow.end").or_(event_name="mf.complex_flow.end")
class PretendThisIsAFlow:
    def __init__(self):
        self._my_attr = "It's Friday!"

    def __str__(self):
        buf = f"{self.__class__.__name__}\n"
        buf = f"{buf}  _my_attr: {self._my_attr}"
        if hasattr(self, "_match_on"):
            buf = f"{buf}\n  match_on: {self._match_on}"
        return buf

f = PretendThisIsAFlow()
print(str(f))