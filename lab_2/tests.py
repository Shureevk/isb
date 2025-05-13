import math
from scipy.special import gammainc
from consts import *

def read_file(filename: str) -> str:
    """
    Чтение последовательности из файла.
    :param filename: Путь к файлу для чтения.
    :return: Прочитанная последовательность.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return ""


def write_file(filename: str, text: str) -> None:
    """
    Запись текста в файл.
    :param filename: Путь к файлу для записи.
    :param text: Текст для записи.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def compute_bit_frequency(sequence: str) -> float:
    """
    Частотный анализ битов.
    :param sequence: Бинарная строка.
    :return: p-значение.
    """
    n = len(sequence)
    s = abs(1 / (math.sqrt(n)) * (sequence.count("1") - sequence.count("0")))
    return math.erfc(s / math.sqrt(2))

def consecutive_runs_test(sequence: str) -> float:
    """
    Тест на одинаково подряд идущие биты.
    :param sequence: Бинарная строка.
    :return: p-значение.
    """
    n = len(sequence)
    p = sequence.count('1') / n

    if abs(p - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v_n = sum(1 for i in range(1, n) if sequence[i] != sequence[i - 1])

    numerator = abs(v_n - 2 * n * p * (1 - p))
    denominator = 2 * math.sqrt(2 * n) * p * (1 - p)
    return math.erfc(numerator / denominator)