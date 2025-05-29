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

def max_consecutive_ones_test(sequence: str) -> float:
    """
    Тест на максимальное количество последовательных единиц в блоке.
    :param sequence: Бинарная строка.
    :return: p-значение.
    """
    n = len(sequence)
    if n < 128:
        raise ValueError("Необходимо минимум 128 бит")

    N = n // 8
    v = [0, 0, 0, 0]

    for i in range(N):
        block = sequence[i * 8 : (i + 1) * 8]
        max_run = 0
        current_run = 0

        for bit in block:
            if bit == '1':
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 0

        if max_run <= 1:
            v[0] += 1
        elif max_run == 2:
            v[1] += 1
        elif max_run == 3:
            v[2] += 1
        else:
            v[3] += 1

    x_2 = sum((v[i] - 16 * PI[i]) ** 2 / (16 * PI[i]) for i in range(len(v)))
    return gammainc(3 / 2, x_2 / 2)

def perform_all_tests(sequence: str, label: str, output_file: str) -> None:
    """
    Выполняет все тесты и сохраняет результат.
    :param sequence: Бинарная строка.
    :param label: Метка для последовательности (например, "C++").
    :param output_file: Путь к файлу для записи результатов.
    """
    p1 = compute_bit_frequency(sequence)
    p2 = consecutive_runs_test(sequence)
    p3 = max_consecutive_ones_test(sequence)

    result = (
        f"{label} последовательность:\n{sequence}\n\n"
        f"Частотный анализ битов (p-значение): {p1:.17f}\n"
        f"Тест на идентичные последовательности битов (p-значение): {p2:.17f}\n"
        f"Тест на максимальное количество последовательных единиц в блоке (p-значение): {p3:.17f}\n"
    )

    write_file(output_file, result)

def main():
    cpp_sequence = read_file(cpp_sequence_txt)
    java_sequence = read_file(java_sequence_txt)
    python_sequence = read_file(python_sequence_txt)

    perform_all_tests(cpp_sequence, "C++", test_results_cpp)
    perform_all_tests(java_sequence, "Java", test_results_java)
    perform_all_tests(python_sequence, "Python", test_results_python)


if __name__ == "__main__":
    main()