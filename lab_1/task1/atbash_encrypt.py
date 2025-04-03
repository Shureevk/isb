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
    original_text = """Я СКАЖУ ТО ЧТО ДЛЯ ТЕБЯ НЕ НОВОСТЬ МИР НЕ ТАКОЙ УЖ СОЛНЕЧНЫЙ И ПРИВЕТЛИВЫЙ ЭТО ОЧЕНЬ ОПАСНОЕ ЖОСТКОЕ МЕСТО И ЕСЛИ ТОЛЬКО ДАШЬ СЛАБИНУ ОН ОПРОКИНЕТ С ТАКОЙ СИЛОЙ ТЕБЯ ЧТО БОЛЬШЕ УЖЕ НЕ ВСТАНЕШЬ НИ ТЫ НИ Я НИКТО НА СВЕТЕ НЕ БЬЕТ ТАК СИЛЬНО КАК ЖИЗНЬ СОВСЕМ НЕ ВАЖНО КАК ТЫ УДАРИШЬ А ВАЖНО КАКОЙ ДЕРЖИШЬ УДАР КАК ДВИГАЕШЬСЯ ВПЕРЕД БУДЕШЬ ИДТИ ИДИ ЕСЛИ С ИСПУГУ НЕ СВЕРНЕШЬ ТОЛЬКО ТАК ПОБЕЖДАЮТ ЕСЛИ ЗНАЕШЬ ЧЕГО ТЫ СТОИШЬ ИДИ И БЕРИ СВОЕ НО БУДЬ ГОТОВ УДАРЫ ДЕРЖАТЬ А НЕ ПЛАКАТЬСЯ И ГОВОРИТЬ Я НИЧЕГО НЕ ДОБИЛСЯ ИЗ ЗА НЕГО ИЗ ЗА НЕЕ ИЗ ЗА КОГО ТО ТАК ДЕЛАЮТ ТРУСЫ А ТЫ НЕ ТРУС БЫТЬ ЭТОГО НЕ МОЖЕТ"""

    encryption_key = create_atbash_key(ALPHABET)

    encrypted_text = encrypt_text(original_text, encryption_key)

    save_to_file('original.txt', original_text)
    save_to_file('encrypted.txt', encrypted_text)
    save_to_file('encryption_key.json', {
        'cipher': 'Atbash',
        'alphabet': ALPHABET,
        'key': encryption_key
    })

    print_results(original_text, encrypted_text, encryption_key)

if __name__ == "__main__":
    main()