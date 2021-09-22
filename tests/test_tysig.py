import unittest
from tysig.tysig import TySig
from typing import Union, Tuple, List, Optional, Dict, Any, AnyStr
from datetime import datetime


@TySig.signature(a=(8, int), b=float, c=str, d=Tuple[str, List[int]])
def fn(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs


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


@TySig.signature(
    name_id=Union[Optional[str], int],
    favnum=(7, int),
    dob=Union[datetime, Tuple[int, int, int]]
)
def fn3(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs


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


@TySig.signature(
    var1=Tuple[str, Any, Any],
    var2=Tuple[Any, Any, str],
    var3=Tuple[Any, Any, Any]
)
def fn5(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs


def print_check(var, ntype, check):
    print("\n", "-" * 30)
    print(f"CHECK: {var} is {ntype} ? --> ", check)
    print("-" * 30)


@TySig.signature(
    var1=Tuple[str, Any, Any],
    var2=Tuple[AnyStr, AnyStr, str],
    var3=Tuple[Any, AnyStr, Any]
)
def fn6(*args, **kwargs):
    print(args)
    print(kwargs)
    return args, kwargs


class TestTySig(unittest.TestCase):
    def test_tuple_union(self):
        AType = Tuple[Union[float, str], Union[int, str], Union[float, str]]
        BType = Tuple[Union[float, str], Union[List[int], str],
                      Union[float, str]]
        a: AType = (2.3, 1, "oik")  # type: ignore
        check = TySig.is_type(a, AType)
        print_check(a, AType, check)
        self.assertEqual(check, True)

        # False example
        check = TySig.is_type(a, BType)
        print_check(a, BType, check)
        self.assertEqual(check, False)

        # False example
        a2: AType = (2.3, 1.6, "oik")
        check = TySig.is_type(a2, AType)
        print_check(a2, AType, check)
        self.assertEqual(check, False)

    def test_dict(self):
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
        self.assertEqual(check, True)

        # False example
        b2: BType = {
            4: (3.7, "je;p", [[4.5, 90.0], {"h": 3.1}, {"pp": 1}, []]),
            5: (3.7, "je;p", [[4.5, 90.2], {"h": 3}, {"pp": 1}, [], {"1": 2}])
        }
        check = TySig.is_type(b2, BType)
        print_check(b2, BType, check)
        self.assertEqual(check, False)

    def test_dict_nested(self):
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
        self.assertEqual(check, True)

        # False example
        c2: CType = {
            "h": {1: {3.3: [({1: 1.}, 5, "hello"), ({3: 1.}, 50, 2.6)]}},
            "ss": {1: {
                3.5: [({1: 1.}, 5., "hello"), ({3: 1.6}, 50.6, "bbbello")]}},
        }
        check = TySig.is_type(c2, CType)
        print_check(c2, CType, check)
        self.assertEqual(check, False)

    def test_optional(self):
        DType = Tuple[Optional[float], Optional[int], Optional[str]]

        d: DType = (2.3, 1, "oik")
        check = TySig.is_type(d, DType)
        print_check(d, DType, check)
        self.assertEqual(check, True)

        d2: DType = (None, 1, "oik")
        check = TySig.is_type(d2, DType)
        print_check(d2, DType, check)
        self.assertEqual(check, True)

        d3: DType = (2.3, None, "oik")
        check = TySig.is_type(d3, DType)
        print_check(d3, DType, check)
        self.assertEqual(check, True)

        d4: DType = (2.3, 1, None)
        check = TySig.is_type(d4, DType)
        print_check(d4, DType, check)
        self.assertEqual(check, True)

        # False example
        d5: DType = (2, 1, None)
        check = TySig.is_type(d5, DType)
        print_check(d5, DType, check)
        self.assertEqual(check, False)

    def test_is_type(self):
        self.assertEqual(TySig.is_type("hello", str), True)
        self.assertEqual(TySig.is_type(44, int), True)
        self.assertEqual(TySig.is_type(3434.3434, float), True)
        self.assertEqual(TySig.is_type([], list), True)
        self.assertEqual(TySig.is_type({1: 2}, dict), True)
        self.assertEqual(TySig.is_type((1, 2), tuple), True)
        self.assertEqual(TySig.is_type("hello", int), False)
        self.assertEqual(TySig.is_type("jhnj", int), False)
        self.assertEqual(TySig.is_type(3434, float), False)
        self.assertEqual(TySig.is_type([], tuple), False)
        self.assertEqual(TySig.is_type({1: 2}, list), False)
        self.assertEqual(TySig.is_type((1, 2), dict), False)

    def test_sig1(self):
        res = fn("hello", ("dd", [1, 2]), b=2.2)
        self.assertEqual(((), {'a': 8, 'c': 'hello',
                               'd': ('dd', [1, 2]), 'b': 2.2}),
                         res)

    def test_sig2(self):
        err = ""
        try:
            _ = fn("hello", ("dd", [1., 2]), b=2.2)
        except TypeError as exp:
            print(exp)
            err = str(exp)
            pass
        self.assertEqual("ARGS: 'd' type should be 'typing.Tuple[str, "
                         "typing.List[int]]' instead found '<class 'tuple'>'"
                         ". If you're using GenericAlias types then please "
                         "check the sub argument types are correct", err)

    def test_sig3(self):
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
        self.assertEqual(((), {
            'idx': 0, 'name': None, 'dob': (2000, 1, 1),
            'ranking': 2.3,
            'history': {
                'gs': (
                    [
                        {
                            1: ['dzf', 'JKkj', 1.0, 'jh', 98.8, 'kj', 2.3,
                                989.0],
                            2: [2.3, 989.0],
                            3: ['dzf', 'JKkj'],
                            4: []
                        },
                        {
                            16: ['dzf', 'JKkj', 1.0, 'jh', 98.8, 'kj', 2.3,
                                 989.0],
                            26: [2.3, 989.0],
                            36: ['dzf', 'JKkj'],
                            46: []
                        }
                    ],
                    98.98,
                    None
                )
            }
        }), res)

    def test_sig4(self):
        err = ""
        try:
            _ = fn2(
                None, (2000, 1, 1), 2.3, history={
                    "gs": [
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
            err = str(exp)
            pass
        exp_error = "KWARGS: 'history' parameter has value of type '<class 'dict'>', " \
                    "but expecting type 'typing.Dict[str, typing.Tuple[typing." \
                    "List[typing.Dict[int, typing.List[typing.Union[str, fl" \
                    "oat]]]], float, typing.Union[int, NoneType]]]'. If you're"\
                    " using GenericAlias types then please check the "\
                    "sub argument types are correct"
        self.assertEqual(exp_error, err)

    def test_sig5(self):
        err = ""
        try:
            _ = fn2(
                None, (2000, 1, "1"), 2.3, history={
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
            err = str(exp)
            pass
        exp_error = "ARGS: 'dob' type should be 'typing.Union[typing.Tuple[int, int," \
                    " int], str]' instead found '<class 'tuple'>'. If you're" \
                    " using GenericAlias types then please check the sub " \
                    "argument types are correct"
        self.assertEqual(exp_error, err)

    def test_sig6(self):
        res = fn3(datetime(2000, 2, 20), name_id=None)
        self.assertEqual(((), {'name_id': None, 'favnum': 7,
                               'dob': datetime(2000, 2, 20)}), res)

    def test_sig7(self):
        res = fn3(8, (2000, 5, 20), name_id=None)
        self.assertEqual(((), {'name_id': None, 'favnum': 8,
                               'dob': (2000, 5, 20)}), res)

    def test_sig8(self):
        res = fn4(None, (2000, 1, 1), 2.3)
        self.assertEqual(((), {
            'idx': 0, 'name': None, 'dob': (2000, 1, 1),
            'ranking': 2.3,
            'history': {"1": ([{1: []}], 0., None)}
        }), res)

    def test_sig9(self):
        res = fn5((2, 3, "d"), ("2.3", "5.6", "sd"), var1=("j", 6, "k"))
        self.assertEqual(
            (
                (),
                {'var2': (2, 3, 'd'), 'var3': ('2.3', '5.6', 'sd'),
                 'var1': ('j', 6, 'k')}
            ),
            res
        )

    def test_sig10(self):
        err = ""
        try:
            _ = fn5(("2", 3, 5), ("2.3", "5.6", "sd"), var1=("j", 6, "k"))
        except TypeError as exp:
            err = str(exp)
            print(err)
        self.assertEqual(
            "ARGS: 'var2' type should be 'typing.Tuple[typing.Any, typing.Any, "
            "str]' instead found '<class 'tuple'>'. If you're using GenericA"
            "lias types then please check the sub argument types are correct",
            err
        )

    def test_sig11(self):
        # var1 = Tuple[str, Any, Any],
        # var2 = Tuple[AnyStr, AnyStr, str],
        # var3 = Tuple[Any, AnyStr, Any]
        res = fn6(("2", b"3", "5"), ("hello", b"5.6", "sd"), var1=("j", 6, "k"))
        self.assertEqual(
            ((), {'var1': ('j', 6, 'k'),
                  'var2': ('2', b'3', '5'),
                  'var3': ('hello', b'5.6', 'sd')}), res)

    def test_sig12(self):
        err = ""
        try:
            _ = fn6(("2", b"3", "5"), (2, 5.6, "sd"), var1=("j", 6, "k"))
        except TypeError as exp:
            err = str(exp)
            print(err)
        self.assertEqual(
            "ARGS: 'var3' type should be 'typing.Tuple[typing.Any, ~AnyStr, "
            "typing.Any]' instead found '<class 'tuple'>'. If you're using "
            "GenericAlias types then please check the sub argument types "
            "are correct",
            err
        )

    def test_sig13(self):
        err = ""
        try:
            _ = fn6(("2", b"3", "5"), (2, b"5.6", "sd"), var1=(6, "k"))
        except TypeError as exp:
            err = str(exp)
            print(err)
        self.assertEqual(
            "KWARGS: 'var1' parameter has value of type '<class 'tuple'>', "
            "but expecting type 'typing.Tuple[str, typing.Any, typing.Any]'. If "
            "you're using GenericAlias types then please check the sub "
            "argument types are correct",
            err
        )
