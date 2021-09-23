# ty-sig

# Type safe checker and signature decorator


```python
from tysig.tysig import TySig
```

## is_type examples

### check type of variable including typing types e.g. Union, Optional, List, Dict, Tuple, Literal, Any, AnyStr, TypeVar, etc.


```python
from typing import Union, Optional, Dict, List, Tuple, Any, AnyStr
```


```python
help(TySig)
```

    Help on class TySig in module tysig.tysig:
    
    class TySig(builtins.object)
     |  Static methods defined here:
     |  
     |  getattr_name(invar) -> Union[str, NoneType]
     |      gets name of type of invar
     |      i.e. gets __name__, or _name, or __origin__ of input object
     |      
     |      :param invar: object we are checking name of
     |      :return: name if exists otherwise None
     |  
     |  is_type(var: object, check_type) -> bool
     |      recursively checks if var is of type check_type
     |      
     |      :param var: variable to check type
     |      :param check_type: type to check against
     |      :return: True if var is of type check_type, else False
     |  
     |  is_typing_type(vtype)
     |      check if type vtype is a typing type of either:
     |      _GenericAlias, _VariadicGenericAlias, or _SpecialForm
     |      
     |      :param vtype: we are checking the type of this type
     |      :return: True if is a typing type, else False
     |  
     |  signature(classobj: bool = False, **in_vars_types)
     |      signature decorator applied to functions to hard check the types
     |      of the arguments including typing types. Also applies default values,
     |      and raises exceptions on failing type checks. Uses is_type function.
     |      
     |      :param classobj: set to True if within a class (self object)
     |      :param in_vars_types: arguments with their types and/or default values
     |                            e.g. @signature(a=int, b=Union[float, str],
     |                                            c=List[Dict[str, Tuple[str, int]]]
     |      :return: applies signature checks and applies default values
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
    
    


```python
def print_check(var, ntype, check):
    print("\n", "-" * 30)
    print(f"CHECK: {var} is {ntype} ? --> ", check)
    print("-" * 30)
```


```python
help(TySig.is_type)
```

    Help on function is_type in module tysig.tysig:
    
    is_type(var: object, check_type) -> bool
        recursively checks if var is of type check_type
        
        :param var: variable to check type
        :param check_type: type to check against
        :return: True if var is of type check_type, else False
    
    


```python
AType = Tuple[Union[float, str], Union[int, str], Union[float, str]]
BType = Tuple[Union[float, str], Union[List[int], str],
          Union[float, str]]
a: AType = (2.3, 1, "oik")  # type: ignore
check = TySig.is_type(a, AType)
print_check(a, AType, check)

# False example
check = TySig.is_type(a, BType)
print_check(a, BType, check)

# False example
a2: AType = (2.3, 1.6, "oik")
check = TySig.is_type(a2, AType)
print_check(a2, AType, check)
```

    
     ------------------------------
    CHECK: (2.3, 1, 'oik') is typing.Tuple[typing.Union[float, str], typing.Union[int, str], typing.Union[float, str]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: (2.3, 1, 'oik') is typing.Tuple[typing.Union[float, str], typing.Union[typing.List[int], str], typing.Union[float, str]] ? -->  False
    ------------------------------
    
     ------------------------------
    CHECK: (2.3, 1.6, 'oik') is typing.Tuple[typing.Union[float, str], typing.Union[int, str], typing.Union[float, str]] ? -->  False
    ------------------------------
    


```python
BType = Dict[
    int,
    Tuple[
        float,
        str,
        List[
            Union[
                Dict[str, int],
                List[float]
            ]
        ]
    ]
]
b: BType = {
    4: (3.7, "je;p", [[4.5, 90.0], {"h": 3}, {"pp": 1}, []]),
    5: (3.7, "je;p", [[4.5, 90.2], {"h": 3}, {"pp": 1}, [], {"1": 2}])
}
check = TySig.is_type(b, BType)
print_check(b, BType, check)

# False example
b2: BType = {
    4: (3.7, "je;p", [[4.5, 90.0], {"h": 3.1}, {"pp": 1}, []]),
    5: (3.7, "je;p", [[4.5, 90.2], {"h": 3}, {"pp": 1}, [], {"1": 2}])
}
check = TySig.is_type(b2, BType)
print_check(b2, BType, check)
```

    
     ------------------------------
    CHECK: {4: (3.7, 'je;p', [[4.5, 90.0], {'h': 3}, {'pp': 1}, []]), 5: (3.7, 'je;p', [[4.5, 90.2], {'h': 3}, {'pp': 1}, [], {'1': 2}])} is typing.Dict[int, typing.Tuple[float, str, typing.List[typing.Union[typing.Dict[str, int], typing.List[float]]]]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: {4: (3.7, 'je;p', [[4.5, 90.0], {'h': 3.1}, {'pp': 1}, []]), 5: (3.7, 'je;p', [[4.5, 90.2], {'h': 3}, {'pp': 1}, [], {'1': 2}])} is typing.Dict[int, typing.Tuple[float, str, typing.List[typing.Union[typing.Dict[str, int], typing.List[float]]]]] ? -->  False
    ------------------------------
    


```python
CType = Dict[str,
             Dict[int,
                  Dict[float,
                       List[
                           Tuple[
                               Dict[int, float],
                               Union[int, float],
                               str
                           ]
                       ]]]]
c: CType = {
    "h": {1: {3.3: [({1: 1.}, 5, "hello"), ({3: 1.}, 50, "bbbello")]}},
    "ss": {1: {
        3.5: [({1: 1.}, 5., "hello"), ({3: 1.6}, 50.6, "bbbello")]}},
}
check = TySig.is_type(c, CType)
print_check(c, CType, check)

# False example
c2: CType = {
    "h": {1: {3.3: [({1: 1.}, 5, "hello"), ({3: 1.}, 50, 2.6)]}},
    "ss": {1: {
        3.5: [({1: 1.}, 5., "hello"), ({3: 1.6}, 50.6, "bbbello")]}},
}
check = TySig.is_type(c2, CType)
print_check(c2, CType, check)
```

    
     ------------------------------
    CHECK: {'h': {1: {3.3: [({1: 1.0}, 5, 'hello'), ({3: 1.0}, 50, 'bbbello')]}}, 'ss': {1: {3.5: [({1: 1.0}, 5.0, 'hello'), ({3: 1.6}, 50.6, 'bbbello')]}}} is typing.Dict[str, typing.Dict[int, typing.Dict[float, typing.List[typing.Tuple[typing.Dict[int, float], typing.Union[int, float], str]]]]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: {'h': {1: {3.3: [({1: 1.0}, 5, 'hello'), ({3: 1.0}, 50, 2.6)]}}, 'ss': {1: {3.5: [({1: 1.0}, 5.0, 'hello'), ({3: 1.6}, 50.6, 'bbbello')]}}} is typing.Dict[str, typing.Dict[int, typing.Dict[float, typing.List[typing.Tuple[typing.Dict[int, float], typing.Union[int, float], str]]]]] ? -->  False
    ------------------------------
    


```python
DType = Tuple[Optional[float], Optional[int], Optional[str]]

d: DType = (2.3, 1, "oik")
check = TySig.is_type(d, DType)
print_check(d, DType, check)

d2: DType = (None, 1, "oik")
check = TySig.is_type(d2, DType)
print_check(d2, DType, check)

d3: DType = (2.3, None, "oik")
check = TySig.is_type(d3, DType)
print_check(d3, DType, check)

d4: DType = (2.3, 1, None)
check = TySig.is_type(d4, DType)
print_check(d4, DType, check)

# False example
d5: DType = (2, 1, None)
check = TySig.is_type(d5, DType)
print_check(d5, DType, check)
```

    
     ------------------------------
    CHECK: (2.3, 1, 'oik') is typing.Tuple[typing.Union[float, NoneType], typing.Union[int, NoneType], typing.Union[str, NoneType]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: (None, 1, 'oik') is typing.Tuple[typing.Union[float, NoneType], typing.Union[int, NoneType], typing.Union[str, NoneType]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: (2.3, None, 'oik') is typing.Tuple[typing.Union[float, NoneType], typing.Union[int, NoneType], typing.Union[str, NoneType]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: (2.3, 1, None) is typing.Tuple[typing.Union[float, NoneType], typing.Union[int, NoneType], typing.Union[str, NoneType]] ? -->  True
    ------------------------------
    
     ------------------------------
    CHECK: (2, 1, None) is typing.Tuple[typing.Union[float, NoneType], typing.Union[int, NoneType], typing.Union[str, NoneType]] ? -->  False
    ------------------------------
    


```python
print(TySig.is_type("hello", str), "Expecting True")
print(TySig.is_type(44, int), "Expecting True")
print(TySig.is_type(3434.3434, float), "Expecting True")
print(TySig.is_type([], list), "Expecting True")
print(TySig.is_type({1: 2}, dict), "Expecting True")
print(TySig.is_type((1, 2), tuple), "Expecting True")
print(TySig.is_type("hello", int), "Expecting False")
print(TySig.is_type("jhnj", int), "Expecting False")
print(TySig.is_type(3434, float), "Expecting False")
print(TySig.is_type([], tuple), "Expecting False")
print(TySig.is_type({1: 2}, list), "Expecting False")
print(TySig.is_type((1, 2), dict), "Expecting False")
```

    True Expecting True
    True Expecting True
    True Expecting True
    True Expecting True
    True Expecting True
    True Expecting True
    False Expecting False
    False Expecting False
    False Expecting False
    False Expecting False
    False Expecting False
    False Expecting False
    

## Signature examples

### Apply signature decorator on top of any function, which will be type-safe - raising exceptions where granular level types are not correct.


```python
help(TySig.signature)
```

    Help on function signature in module tysig.tysig:
    
    signature(classobj: bool = False, **in_vars_types)
        signature decorator applied to functions to hard check the types
        of the arguments including typing types. Also applies default values,
        and raises exceptions on failing type checks. Uses is_type function.
        
        :param classobj: set to True if within a class (self object)
        :param in_vars_types: arguments with their types and/or default values
                              e.g. @signature(a=int, b=Union[float, str],
                                              c=List[Dict[str, Tuple[str, int]]]
        :return: applies signature checks and applies default values
    
    

### Working and Non-Working examples below


```python
@TySig.signature(a=(8, int), b=float, c=str, d=Tuple[str, List[int]])
def fn(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs
```


```python
# working example where the data within the data structures conform to the signature
res = fn("hello", ("dd", [1, 2]), b=2.2)
print(res == ((), {'a': 8, 'c': 'hello', 'd': ('dd', [1, 2]), 'b': 2.2}))
```

    ()
    {'a': 8, 'c': 'hello', 'd': ('dd', [1, 2]), 'b': 2.2}
    True
    


```python
# non-working example where the data within the data structures do not conform to the signature
try:
    _ = fn("hello", ("dd", [1., 2]), b=2.2)  # list within tuple is only allowed to hold int's
except TypeError as exp:
    print(exp)
```

    'd' type should be 'typing.Tuple[str, typing.List[int]]' instead found '<class 'tuple'>'. If you're using GenericAlias, VariadicGenericAlias, or SpecialForm types then please check the sub argument types are correct
    


```python
@TySig.signature(
    idx=(0, int),
    name=Optional[str],
    dob=Union[Tuple[int, int, int], str],
    history=Dict[str, Tuple[List[Dict[int, List[Union[str, float]]]],
                            float, Optional[int]]],
    ranking=float
)
def fn2(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs
```


```python
# working example where the data within the data structures conform to the signature
res = fn2(
    None, (2000, 1, 1), 2.3, history={
        "gs": (
            [
                {
                    1: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3, 989.],
                    2: [2.3, 989.],
                    3: ["dzf", "JKkj"],
                    4: []
                },
                {
                    16: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3,
                         989.],
                    26: [2.3, 989.],
                    36: ["dzf", "JKkj"],
                    46: []
                }
            ], 98.98, None
        )
    }
)
```

    ()
    {'idx': 0, 'name': None, 'dob': (2000, 1, 1), 'ranking': 2.3, 'history': {'gs': ([{1: ['dzf', 'JKkj', 1.0, 'jh', 98.8, 'kj', 2.3, 989.0], 2: [2.3, 989.0], 3: ['dzf', 'JKkj'], 4: []}, {16: ['dzf', 'JKkj', 1.0, 'jh', 98.8, 'kj', 2.3, 989.0], 26: [2.3, 989.0], 36: ['dzf', 'JKkj'], 46: []}], 98.98, None)}}
    


```python
# non-working example where the data within the data structures do not conform to the signature
try:
    _ = fn2(
        None, (2000, 1, 1), 2.3, history={
            "gs": [  # this part of 'history' a list but should be tuple as per signature
                [
                    {
                        1: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3,
                            989.],
                        2: [2.3, 989.],
                        3: ["dzf", "JKkj"],
                        4: []
                    },
                    {
                        16: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3,
                             989.],
                        26: [2.3, 989.],
                        36: ["dzf", "JKkj"],
                        46: []
                    }
                ], 98.98, None
            ]
        }
    )
except TypeError as exp:
    print(exp)
```

    'history' type should be 'typing.Dict[str, typing.Tuple[typing.List[typing.Dict[int, typing.List[typing.Union[str, float]]]], float, typing.Union[int, NoneType]]]' instead found '<class 'dict'>'. If you're using GenericAlias, VariadicGenericAlias, or SpecialForm types then please check the sub argument types are correct
    


```python
# non-working example where the data within the data structures do not conform to the signature
try:
    _ = fn2(
        None, (2000, 1, "1"), 2.3, history={  # dob tuple, last element is str but should be int
            "gs": (
                [
                    {
                        1: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3,
                            989.],
                        2: [2.3, 989.],
                        3: ["dzf", "JKkj"],
                        4: []
                    },
                    {
                        16: ["dzf", "JKkj", 1., "jh", 98.8, "kj", 2.3,
                             989.],
                        26: [2.3, 989.],
                        36: ["dzf", "JKkj"],
                        46: []
                    }
                ], 98.98, None
            )
        }
    )
except TypeError as exp:
    print(exp)
```

    'dob' type should be 'typing.Union[typing.Tuple[int, int, int], str]' instead found '<class 'tuple'>'. If you're using GenericAlias, VariadicGenericAlias, or SpecialForm types then please check the sub argument types are correct
    


```python
from datetime import datetime
```


```python
@TySig.signature(
    name_id=Union[Optional[str], int],
    favnum=(7, int),
    dob=Union[datetime, Tuple[int, int, int]]
)
def fn3(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs
```


```python
# working examples where the data within the data structures conform to the signature
_ = fn3(datetime(2000, 2, 20), name_id=None)
_ = fn3(8, (2000, 5, 20), name_id=None)
```

    ()
    {'favnum': 7, 'dob': datetime.datetime(2000, 2, 20, 0, 0), 'name_id': None}
    ()
    {'favnum': 8, 'dob': (2000, 5, 20), 'name_id': None}
    


```python
@TySig.signature(
    idx=(0, int),
    name=Optional[str],
    dob=Union[Tuple[int, int, int], str],
    history=(
            {"1": ([{1: []}], 0., None)},
            Dict[str, Tuple[List[Dict[int, List[Union[str, float]]]],
                            float, Optional[int]]]
    ),
    ranking=float
)
def fn4(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs
```


```python
# working example where the data within the data structures conform to the signature
_ = fn4(None, (2000, 1, 1), 2.3)
```

    ()
    {'idx': 0, 'name': None, 'dob': (2000, 1, 1), 'history': {'1': ([{1: []}], 0.0, None)}, 'ranking': 2.3}
    


```python
@TySig.signature(
    var1=Tuple[str, Any, Any],
    var2=Tuple[AnyStr, Any, str],
    var3=Tuple[Any, AnyStr, Any]
)
def fn5(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs
```


```python
# working example where the data within the data structures conform to the signature
_ = fn5((b"2", 3, "d"), ("2.3", b"5.6", "sd"), var1=("j", 6, "k"))
```

    ()
    {'var2': (b'2', 3, 'd'), 'var3': ('2.3', b'5.6', 'sd'), 'var1': ('j', 6, 'k')}
    


```python
# non-working example where the data within the data structures do not conform to the signature
try:
    _ = fn5((2, 3, "5"), (2.3, "5.6", "sd"), var1=("j", 6, "k"))
except TypeError as exp:
    print(exp)
```

    'var2' type should be 'typing.Tuple[~AnyStr, typing.Any, str]' instead found '<class 'tuple'>'. If you're using GenericAlias, VariadicGenericAlias, or SpecialForm types then please check the sub argument types are correct
    


```python
# non-working example where the data within the data structures do not conform to the signature
try:
    _ = fn5((b"2", 3, "5"), ("2.3", b"5.6"), var1=("j", 6, "k"))
except TypeError as exp:
    print(exp)
```

    'var3' type should be 'typing.Tuple[typing.Any, ~AnyStr, typing.Any]' instead found '<class 'tuple'>'. If you're using GenericAlias, VariadicGenericAlias, or SpecialForm types then please check the sub argument types are correct
    
