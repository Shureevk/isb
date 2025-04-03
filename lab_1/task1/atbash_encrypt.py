import json
import os
from constants import ALPHABET, FILE_ORIGINAL_TEXT, FILE_ENCRYPTED_TEXT, FILE_ENCRYPTION_KEY

def create_atbash_key(alphabet):
    """Создание ключа шифрования Атбаш

    :param alphabet: алфавит для шифрования
    :return: словарь подстановки символов
    """
    return {original: cipher for original, cipher in zip(alphabet, alphabet[::-1])}

def encrypt_text(text, key):
    """Шифрование текста

    :param text: исходный текст
    :param key: ключ шифрования
    :return: зашифрованный текст
    """
    return ''.join([key.get(char, char) for char in text])

def save_to_file(filename, data):
    """Сохранение данных в файл

    :param filename: путь к файлу
    :param data: данные для сохранения
    """
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)  # Создаём папку, если её нет
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, str):
                f.write(data)
            else:
                json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении в файл {filename}: {e}")

def load_text_from_file(filename):
    """Загрузка текста из файла с обработкой ошибок"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении файла {filename}: {e}")
    return ""

def print_results(original, encrypted, key):
    """Вывод результатов шифрования в консоль

    :param original: исходный текст
    :param encrypted: зашифрованный текст
    :param key: ключ шифрования
    """
    print("="*50)
    print("Исходный текст:")
    print("="*50)
    print(original)

    print("\n" + "="*50)
    print("Зашифрованный текст:")
    print("="*50)
    print(encrypted)

    print("\n" + "="*50)
    print("Первые 10 пар ключа:")
    print("="*50)
    for i, (k, v) in enumerate(key.items()):
        if i >= 10:
            break
        print(f"{k} → {v}")

def main():
    """Основная логика программы"""
    original_text = load_text_from_file(FILE_ORIGINAL_TEXT)
    if not original_text:
        print("Ошибка: Исходный текст не загружен.")
        return

    encryption_key = create_atbash_key(ALPHABET)
    encrypted_text = encrypt_text(original_text, encryption_key)

    save_to_file(FILE_ENCRYPTED_TEXT, encrypted_text)
    save_to_file(FILE_ENCRYPTION_KEY, {
        'cipher': 'Atbash',
        'alphabet': ALPHABET,
        'key': encryption_key
    })

    print_results(original_text, encrypted_text, encryption_key)


if __name__ == "__main__":
    main() 
