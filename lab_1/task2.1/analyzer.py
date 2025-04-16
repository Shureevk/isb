from collections import defaultdict
import argparse
import sys
import json
from pathlib import Path
from constants import DEFAULT_INPUT_FILE, DEFAULT_OUTPUT_FILE, DEFAULT_DECRYPTED_FILE


def load_decryption_key(key_path: str = "decryption_key.json") -> dict:
    """Загрузка ключа расшифровки из JSON-файла

    :param key_path: путь к JSON-файлу с ключом расшифровки
    :return: словарь с ключом подстановки символов
    """
    try:
        with open(key_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл с ключом '{key_path}' не найден!")
    except json.JSONDecodeError:
        raise ValueError(f"Файл '{key_path}' содержит невалидный JSON!")


def read_file(filename: str) -> str:
    """Чтение содержимого файла

    :param filename: путь к файлу для чтения
    :return: содержимое файла в виде строки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        if not text:
            raise ValueError("Файл пуст!")
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл '{filename}' не найден!")
    except PermissionError:
        raise PermissionError(f"Нет доступа к файлу '{filename}'!")
    except UnicodeDecodeError:
        raise UnicodeDecodeError(f"Файл '{filename}' имеет неверную кодировку (ожидается UTF-8)!")


def write_file(content: str, output_file: str) -> None:
    """Запись содержимого в файл

    :param content: строка для записи
    :param output_file: путь к выходному файлу
    """
    try:
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
    except PermissionError:
        raise PermissionError(f"Нет доступа для записи в файл '{output_file}'!")


def calculate_frequencies(text: str) -> tuple[list[tuple[str, int]], int]:
    """Вычисление частоты символов в тексте

    :param text: анализируемый текст
    :return: отсортированный список пар символ-частота, общее количество символов
    """
    frequencies = defaultdict(int)
    total_symbols = 0

    for char in text:
        frequencies[char] += 1
        total_symbols += 1

    if total_symbols == 0:
        raise ValueError("Нет символов для анализа!")

    sorted_frequencies = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    return sorted_frequencies, total_symbols


def format_frequencies(frequencies: list[tuple[str, int]], total_symbols: int) -> str:
    """Форматирование результатов анализа частот

    :param frequencies: список пар символ-количество
    :param total_symbols: общее количество символов
    :return: отформатированная строка с результатами
    """
    lines = [
        f"Всего символов: {total_symbols}\n",
        "Символ | Количество | Частота (%)",
        "--------------------------------"
    ]

    for char, count in frequencies:
        frequency = (count / total_symbols) * 100
        char_repr = repr(char)[1:-1] if char in {'\n', '\t', '\r'} else char
        lines.append(f"'{char_repr}'   | {count:9} | {frequency:.2f}%")

    return "\n".join(lines)


def decrypt_file(input_file: str, output_file: str, key_path: str = "decryption_key.json") -> None:
    """Расшифровка файла с использованием ключа подстановки

    :param input_file: путь к зашифрованному файлу
    :param output_file: путь для сохранения расшифрованного файла
    :param key_path: путь к JSON-файлу с ключом
    """
    try:
        decryption_key = load_decryption_key(key_path)

        encrypted_text = read_file(input_file)

        decrypted_text = ''.join([decryption_key.get(char, char) for char in encrypted_text])

        write_file(decrypted_text, output_file)
        print(f"Файл успешно расшифрован. Результат сохранён в '{output_file}'")

    except Exception as e:
        print(f"Ошибка при расшифровке: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Анализатор частоты символов и дешифратор текста",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "input_file",
        help=f"Путь к входному файлу (по умолчанию: {DEFAULT_INPUT_FILE})",
        default=DEFAULT_INPUT_FILE,
        nargs='?'
    )
    parser.add_argument(
        "-o", "--output",
        help=f"Путь к выходному файлу (по умолчанию: {DEFAULT_OUTPUT_FILE})",
        default=DEFAULT_OUTPUT_FILE
    )
    parser.add_argument(
        "-d", "--decrypt",
        help="Активировать режим расшифровки",
        action="store_true"
    )
    parser.add_argument(
        "--decrypted-output",
        help=f"Файл для сохранения расшифрованного текста (по умолчанию: {DEFAULT_DECRYPTED_FILE})",
        default=DEFAULT_DECRYPTED_FILE
    )
    parser.add_argument(
        "-k", "--key",
        help="Путь к JSON-файлу с ключом расшифровки (по умолчанию: decryption_key.json)",
        default="decryption_key.json"
    )
    args = parser.parse_args()

    try:
        if args.decrypt:
            decrypt_file(args.input_file, args.decrypted_output, args.key)
        else:
            text = read_file(args.input_file)
            frequencies, total_symbols = calculate_frequencies(text)
            result = format_frequencies(frequencies, total_symbols)
            print(result)
            write_file(result, args.output)
            print(f"\nРезультаты анализа сохранены в '{args.output}'")

    except Exception as e:
        print(f"Ошибка: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()