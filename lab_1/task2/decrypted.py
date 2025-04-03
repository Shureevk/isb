import json
import os
import collections
from constants import ALPHABET, RUSSIAN_FREQUENCIES, FILE_ENCRYPTED_TEXT, FILE_DECRYPTED_TEXT, FILE_DECRYPTION_KEY

def decrypt_cipher(cipher_text: str, alphabet: str, frequencies: list) -> tuple[str, dict]:
    """Дешифрование методом частотного анализа."""
    cipher_freq = collections.Counter(cipher_text)
    sorted_cipher_freq = [char for char, _ in cipher_freq.most_common()]

    decryption_key = {enc_char: dec_char for (dec_char, _), enc_char in zip(frequencies, sorted_cipher_freq)}
    decoded_text = "".join(decryption_key.get(c, c) for c in cipher_text)

    return decoded_text, decryption_key

def read_file(filename: str) -> str:
    """Читает содержимое файла."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Ошибка: файл {filename} не найден.")
    except Exception as e:
        print(f"Ошибка при чтении {filename}: {e}")
    return ""

def save_to_file(filename: str, data):
    """Сохраняет данные в файл, создавая папку при необходимости."""
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as file:
            if isinstance(data, str):
                file.write(data)
            else:
                json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Ошибка при записи в {filename}: {e}")

def main():
    """Основная логика программы."""
    encrypted_text = read_file(FILE_ENCRYPTED_TEXT)
    if not encrypted_text:
        print("Ошибка: зашифрованный текст не загружен.")
        return

    decrypted_text, decryption_key = decrypt_cipher(encrypted_text, ALPHABET, RUSSIAN_FREQUENCIES)

    save_to_file(FILE_DECRYPTED_TEXT, decrypted_text)
    save_to_file(FILE_DECRYPTION_KEY, decryption_key)

    print("Дешифровка завершена. Файлы сохранены.")

if __name__ == "__main__":
    main()
