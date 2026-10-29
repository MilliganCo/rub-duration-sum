import re
import sys
from typing import Optional, List


def extract_rub_amounts(text: str, duration: Optional[str] = None) -> List[int]:
    """
    Извлекает суммы (числа перед '₽'), которые относятся к блоку после срока (например "2д 8ч" или "5ч"),
    но пропускает блок, если ПОСЛЕ срока раньше суммы встречается слово "Бесплатно".

    Если duration задан (например "2д 8ч") — учитываются только такие сроки.
    """
    text = text.replace("\u00A0", " ")  # неразрывные пробелы -> обычные

    # Every duration is a segment boundary, even when filtering one duration.
    dur_rx = re.compile(r"\b(?:\d+д\s*\d+ч|\d+ч)\b")
    wanted = re.sub(r"\s+", "", duration) if duration is not None else None

    amt_rx = re.compile(r"(?P<amt>\d[\d ]*)\s*₽")
    free_rx = re.compile(r"\bБесплатно\b")

    dur_matches = list(dur_rx.finditer(text))
    amounts: List[int] = []

    for i, m in enumerate(dur_matches):
        if wanted is not None and re.sub(r"\s+", "", m.group()) != wanted:
            continue
        seg_start = m.end()
        seg_end = dur_matches[i + 1].start() if i + 1 < len(dur_matches) else len(text)
        segment = text[seg_start:seg_end]

        # Ищем, что встретится раньше в сегменте: "Бесплатно" или сумма "NN ₽"
        free_m = free_rx.search(segment)
        amt_m = amt_rx.search(segment)

        if free_m and (not amt_m or free_m.start() < amt_m.start()):
            # Бесплатно встретилось раньше первой суммы -> пропускаем этот срок/блок
            continue

        if amt_m:
            amt = int(re.sub(r"\D", "", amt_m.group("amt")))  # убрать пробелы
            amounts.append(amt)

    return amounts


def main():
    # укажите имя файла рядом со скриптом
    with open("input.txt", "r", encoding="utf-8") as f:
        text = f.read()

    amounts = extract_rub_amounts(text)
    print("Найденные суммы:", amounts)
    print("Итого:", sum(amounts), "₽")



if __name__ == "__main__":
    main()
