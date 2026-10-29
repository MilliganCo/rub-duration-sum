import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sum_rub', Path(__file__).parents[1] / 'sum_rub.py')
parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser)


class AmountTests(unittest.TestCase):
    def test_whole_rubles_nbsp_and_free_block(self):
        text = '2д 8ч 1\u00a0200 ₽\n5ч Бесплатно 700 ₽\n6ч 300 ₽'
        self.assertEqual(parser.extract_rub_amounts(text), [1200, 300])

    def test_specific_duration_cannot_consume_a_later_different_block(self):
        self.assertEqual(parser.extract_rub_amounts('5ч без цены\n6ч 900 ₽', duration='5ч'), [])

    def test_duration_filter_and_amount_before_free_label(self):
        text = '5ч 100 ₽ Бесплатно\n6ч 200 ₽\n5ч 300 ₽'
        self.assertEqual(parser.extract_rub_amounts(text, duration='5ч'), [100, 300])

    def test_no_duration_or_no_amount_has_no_result(self):
        self.assertEqual(parser.extract_rub_amounts('Цена 500 ₽ без срока'), [])
        self.assertEqual(parser.extract_rub_amounts('5ч без цены'), [])


if __name__ == '__main__':
    unittest.main()
