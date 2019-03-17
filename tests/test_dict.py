import datetime
from typing import Dict
from unittest import TestCase
import jsons
from jsons import DeserializationError


class TestDict(TestCase):
    def test_load_dict(self):
        dumped = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        loaded = jsons.load(dumped)
        self.assertEqual(loaded['a']['b']['c']['d'].year, 2018)
        self.assertEqual(loaded['a']['b']['c']['d'].month, 7)
        self.assertEqual(loaded['a']['b']['c']['d'].day, 8)
        self.assertEqual(loaded['a']['b']['c']['d'].hour, 21)
        self.assertEqual(loaded['a']['b']['c']['d'].minute, 34)
        self.assertEqual(loaded['a']['b']['c']['d'].second, 0)

    def test_load_dict_with_generic(self):
        class A:
            def __init__(self):
                self.name = 'A'

        class B:
            def __init__(self, a: A):
                self.a = a
                self.name = 'B'

        dumped_b = {'a': {'name': 'A'}, 'name': 'B'}
        dumped_dict = {'b_inst': dumped_b}
        loaded = jsons.load(dumped_dict, Dict[str, B])

        self.assertEqual(loaded['b_inst'].a.name, 'A')

    def test_load_partially_deserialized_dict(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        loaded = jsons.load(dumped, C)

        self.assertEqual(loaded.d, dat)

    def test_load_partially_deserialized_dict_in_strict_mode(self):
        class C:
            def __init__(self, d: datetime.datetime):
                self.d = d

        dat = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                                tzinfo=datetime.timezone.utc)
        dumped = {'d': dat}
        with self.assertRaises(DeserializationError):
            jsons.load(dumped, C, strict=True)

    def test_dump_dict(self):
        d = datetime.datetime(year=2018, month=7, day=8, hour=21, minute=34,
                              tzinfo=datetime.timezone.utc)
        dict_ = {'a': {'b': {'c': {'d': d}}}}
        expectation = {'a': {'b': {'c': {'d': '2018-07-08T21:34:00Z'}}}}
        self.assertDictEqual(expectation, jsons.dump(dict_))
