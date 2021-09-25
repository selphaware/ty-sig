"""
    (c) 2021 Usman Ahmad https://github.com/selphaware

    tyerrors.py

    Error messages used by tysig.py
"""


DEFAULT_ERROR = "'{}' default value is of type '{}', but expecting type '{}'"

SIG_TYPE_ERROR = "Expected type or tuple in signature instead found '{}'"

ARGS_ERROR = "'{}' type should be '{}' instead found '{}'. If "\
             "you're using GenericAlias, VariadicGenericAlias, or SpecialForm"\
             " types then please check the sub argument types are correct"

UNEXP_ERROR = "Found unexpected extra arguments: {}"

RET_TYPE_ERROR = "Return object type does not match signature return type {}"
