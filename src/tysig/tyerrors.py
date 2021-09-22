"""
    (c) 2021 Usman Ahmad https://github.com/selphaware

    tyerrors.py

    Error messages used by tysig.py
"""


DEFAULT_ERROR = "'{}' default value is of type '{}', but expecting type '{}'"

SIG_TYPE_ERROR = "Expected type or tuple in signature instead found '{}'"

KWARGS_ERROR = "KWARGS: '{}' parameter has value of type '{}', but expecting "\
               "type '{}'. If you're using GenericAlias, VariadicGenericAlias"\
               ", or SpecialForm types then please check the sub argument "\
               "types are correct"

ARGS_ERROR = "ARGS: '{}' type should be '{}' instead found '{}'. If "\
             "you're using GenericAlias, VariadicGenericAlias, or SpecialForm"\
             " types then please check the sub argument types are correct"

UNEXP_ERROR = "Found unexpected extra arguments: {}"
