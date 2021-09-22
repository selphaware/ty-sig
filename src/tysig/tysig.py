"""
    (c) 2021 Usman Ahmad https://github.com/selphaware

    tysig.py

    Type Safe checker and signature decorator for type checking and
    typing type checking e.g. Union, Optional, Literal, Any, AnyStr,
    Tuple, Dict, List, TypeVar
"""


from typing import Union, Optional, TypeVar, _GenericAlias, \
    _SpecialForm, _VariadicGenericAlias, Callable
from functools import wraps


class TySig(object):

    @staticmethod
    def is_type(
            var: object,
            check_type: Union[
                type, TypeVar, _GenericAlias,
                _SpecialForm, _VariadicGenericAlias
            ]
    ) -> bool:
        """
        recursively checks if var is of type check_type

        :param var: variable to check type
        :param check_type: type to check against
        :return: True if var is of type check_type, else False
        """
        try:
            return isinstance(var, check_type)
        except TypeError:
            pass
        type_dict = check_type.__dict__
        if len(type_dict) == 0:  # Any, AnyStr, Literal type
            return True
        else:
            type_args = type_dict['__args__']
            type_origin = type_dict['__origin__']

            if (type_origin is Union) or (type_origin is Optional):
                correct_type = any(TySig.is_type(var, x) for x in type_args)

            elif (type_origin is list) and (isinstance(var, list)):
                correct_type = all(TySig.is_type(x, type_args[0]) for x in var)

            elif (type_origin is tuple) and (isinstance(var, tuple)):
                correct_type = all(TySig.is_type(x, type_args[i])
                                   for i, x in enumerate(var))

            elif (type_origin is dict) and (isinstance(var, dict)):
                correct_keys = all(TySig.is_type(x, type_args[0])
                                   for x in var.keys())
                correct_vals = all(TySig.is_type(x, type_args[1])
                                   for x in var.values())
                correct_type = correct_keys and correct_vals
            else:
                correct_type = False

            return correct_type

    @staticmethod
    def signature(classobj: bool = False, **in_vars_types):
        """
        signature decorator applied to functions to hard check the types
        of the arguments including typing types. Also applies default values,
        and raises exceptions on failing type checks. Uses is_type function.

        :param classobj: set to True if within a class (self object)
        :param in_vars_types: arguments with their types and/or default values
                              e.g. @signature(a=int, b=Union[float, str],
                                              c=List[Dict[str, Tuple[str, int]]]
        :return: applies signature checks and applies default values
        """
        def inner(fun: Callable):
            @wraps(fun)
            def sub(*_in_args, **in_kwargs):
                in_args = _in_args[1:] if classobj else _in_args
                istype = TySig.is_type
                vars_types = in_vars_types.copy()
                kwargs = in_kwargs.copy()
                args = [x for x in in_args]

                # check default arguments which are of type tuple e.g. (2, int)
                defmap = dict()
                for vname, vdeftype in vars_types.items():
                    if isinstance(vdeftype, tuple):
                        vdef, vtype = vdeftype
                        if not istype(*vdeftype):
                            raise TypeError(f"'{vname}' default value is of "
                                            f"type '{type(vdef)}', but "
                                            f"expecting type '{vtype}'")
                        else:
                            defmap[vname] = vdef

                def get_def_type(in_vdeftype) -> tuple:
                    if isinstance(in_vdeftype, type) or (
                            isinstance(in_vdeftype, _GenericAlias)):
                        in_vdef, in_vtype = None, in_vdeftype
                    elif isinstance(in_vdeftype, tuple):
                        in_vdef, in_vtype = in_vdeftype
                    else:
                        raise TypeError("Expected type or tuple in signature "
                                        f"instead found '{type(in_vdeftype)}'")
                    return in_vdef, in_vtype

                # check kwargs
                _kwargs = kwargs.copy()
                for kw_name, kw_val in _kwargs.items():
                    vdeftype = vars_types.get(kw_name)
                    if vdeftype is None:
                        raise TypeError(f"Unexpected variable found: '{kw_name}'")

                    _, vtype = get_def_type(vdeftype)
                    if not istype(kw_val, vtype):
                        raise TypeError(f"'{kw_name}' parameter has value of "
                                        f"type '{type(kw_val)}', but "
                                        f"expecting type '{vtype}'")
                    kwargs.pop(kw_name)
                    vars_types.pop(kw_name)

                # check args
                for vname, vdeftype in vars_types.items():
                    vdef, vtype = get_def_type(vdeftype)
                    selected_arg = False
                    idx = -1
                    for idx, arg in enumerate(args):
                        if not istype(arg, vtype):
                            if vdef is None:
                                raise TypeError(f"'{vname}' type should be "
                                                f"'{vtype}' instead found "
                                                f"'{type(arg)}'. If you're "
                                                "using GenericAlias types then"
                                                " please check the sub "
                                                "argument types are correct")
                            else:
                                kwargs[vname] = vdef
                                break
                        else:
                            kwargs[vname] = arg
                            selected_arg = True
                            break
                    if selected_arg and (idx >= 0):
                        del args[idx]

                # finalize kwargs, apply defaults, and execute function
                kwargs.update(in_kwargs)
                for vname, vdef in defmap.items():
                    if kwargs.get(vname) is None:
                        kwargs[vname] = vdef

                # final check to see if there are any remaining args
                if len(args) > 0:
                    raise TypeError(f"Found unexpected extra arguments: {args}")

                # if running in a class then pass through self class object
                if classobj:
                    return fun(_in_args[0], **kwargs)
                else:  # otherwise: run function normally passing through all set args
                    return fun(**kwargs)
            return sub
        return inner
