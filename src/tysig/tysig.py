"""
    (c) 2021 Usman Ahmad https://github.com/selphaware

    tysig.py

    Type Safe checker and signature decorator for type checking and
    typing type checking e.g. Union, Optional, Literal, Any, AnyStr,
    Tuple, Dict, List, TypeVar
"""

from typing import Union, Optional, Callable
import typing
from functools import wraps
from tysig.tyerrors import DEFAULT_ERROR, SIG_TYPE_ERROR, ARGS_ERROR, \
    UNEXP_ERROR


class TySig(object):

    @staticmethod
    def getattr_name(invar) -> Optional[str]:
        """
        gets name of type of invar
        i.e. gets __name__, or _name, or __origin__ of input object

        :param invar: object we are checking name of
        :return: name if exists otherwise None
        """
        ftype = None
        try:
            ftype = invar.__getattribute__('_name')
        except (AttributeError, TypeError):
            try:
                ftype = invar.__getattribute__('__name__')
            except (AttributeError, TypeError):
                pass
        if ftype is None:
            try:
                ftype = str(invar.__getattribute__('__origin__'))
                if "typing." in ftype:
                    ftype = ftype.split('.')[1]
            except (AttributeError, TypeError):
                pass
        return ftype

    @staticmethod
    def is_type(
            var: object,
            check_type
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
        if len(type_dict) == 0:
            attr = TySig.getattr_name(check_type)
            if attr == "Any":
                return True
            elif attr == "AnyStr":
                return isinstance(var, str) or isinstance(var, bytearray) \
                       or isinstance(var, bytes)
            else:  # None or otherwise
                return False
        else:
            type_args = type_dict['__args__']
            type_origin = type_dict['__origin__']

            if (type_origin is Union) or (type_origin is Optional):
                correct_type = any(TySig.is_type(var, x) for x in type_args)

            elif (type_origin is list) and (isinstance(var, list)):
                correct_type = all(TySig.is_type(x, type_args[0]) for x in var)

            elif (type_origin is tuple) and (isinstance(var, tuple)):
                if len(var) == len(type_args):
                    correct_type = all(TySig.is_type(x, type_args[i])
                                       for i, x in enumerate(var))
                else:
                    correct_type = False

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
    def is_typing_type(vtype):
        """
        check if type vtype is a typing type of either:
        _GenericAlias, _VariadicGenericAlias, or _SpecialForm

        :param vtype: we are checking the type of this type
        :return: True if is a typing type, else False
        """
        type_name = TySig.getattr_name(vtype)
        typing_types = [x for x in typing.__dict__['__all__'] if x[0].isupper()]
        return type_name in typing_types

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
                # initialise vars_types (signature params), kwargs, args
                in_args = _in_args[1:] if classobj else _in_args
                istype = TySig.is_type
                vars_types = in_vars_types.copy()
                kwargs = in_kwargs.copy()
                args = [x for x in in_args]
                _NO_DEF = "__NO_DEF__"

                # check default types which are of type tuple e.g. (2, int)
                defmap = dict()
                for vname, vdeftype in vars_types.items():
                    if isinstance(vdeftype, tuple):
                        vdef, vtype = vdeftype
                        if not istype(*vdeftype):
                            raise TypeError(
                                DEFAULT_ERROR.format(vname, type(vdef), vtype)
                            )
                        else:
                            defmap[vname] = vdef

                # function to get the type and default value
                # _NO_DEF represents no default value
                def get_def_type(in_vdeftype) -> tuple:
                    if TySig.is_typing_type(in_vdeftype) or \
                            isinstance(in_vdeftype, type):
                        in_vdef, in_vtype = _NO_DEF, in_vdeftype
                    elif isinstance(in_vdeftype, tuple):
                        in_vdef, in_vtype = in_vdeftype
                    else:
                        raise TypeError(
                            SIG_TYPE_ERROR.format(type(in_vdeftype)))
                    return in_vdef, in_vtype

                # check types in kwargs
                # if types are good then pop from kwargs
                _kwargs = kwargs.copy()
                for kw_name, kw_val in _kwargs.items():
                    vdeftype = vars_types.get(kw_name)
                    if vdeftype is None:
                        raise TypeError(
                            f"Unexpected variable found: '{kw_name}'")

                    # we don't care about default values here (handled below)
                    # we are checking if kwarg types are correct
                    _, vtype = get_def_type(vdeftype)
                    if not istype(kw_val, vtype):
                        raise TypeError(ARGS_ERROR.format(kw_name, vtype,
                                                          type(kw_val)))
                    kwargs.pop(kw_name)
                    vars_types.pop(kw_name)

                # assign values from args to kwargs
                # go through all signature params and compare against args
                for vname, vdeftype in vars_types.items():
                    vdef, vtype = get_def_type(vdeftype)
                    selected_arg = False
                    idx = -1
                    # compare signature type against types of args
                    for idx, arg in enumerate(args):
                        # if type matches, assign value or default
                        if not istype(arg, vtype):
                            if vdef == _NO_DEF:
                                raise TypeError(
                                    ARGS_ERROR.format(vname, vtype, type(arg)))
                            else:  # assign default
                                kwargs[vname] = vdef
                                break
                        # type matches, assign value in kwargs
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
                    raise TypeError(UNEXP_ERROR.format(args))

                # if running in a class then pass through self class object
                if classobj:
                    return fun(_in_args[0], **kwargs)
                else:  # ow: run function normally passing through all set args
                    return fun(**kwargs)

            return sub

        return inner
