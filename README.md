# Ruble Duration Sum

Extract whole-ruble amounts from duration blocks, with free-block handling and exact-duration filtering.

Python 3.10+, standard library only. Copy input.example.txt to a private ignored input.txt,
edit the text, then run `python sum_rub.py`. The function `extract_rub_amounts(text, duration=None)`
can also filter one duration. Every duration remains a boundary, so another block's price is not
accidentally counted when filtering. “Бесплатно” before the first price excludes that block.
This parser targets whole-ruble tariff text; decimal/fractional prices are outside its format.

See VALIDATION.md for actual checks.
