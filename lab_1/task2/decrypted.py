import json
import collections

def decrypt_cipher(cipher_text: str) -> tuple[str, dict]:
    """Дешифрование текста методом простой подстановки (моноалфавитная замена).

    :param cipher_text: зашифрованный текст
    :return: кортеж из дешифрованного текста и словаря ключей расшифровки
    """
    alphabet = "АБВГДЕЖЗИЙКЛМОПРСТУФХЦЧШЩЪЫЬЭЮЯ "

    russian_frequencies = [
        (' ', 0.128675), ('О', 0.096456), ('И', 0.075312), ('Е', 0.072292),
        ('А', 0.064841), ('Н', 0.061820), ('Т', 0.061619), ('С', 0.051953),
        ('Р', 0.040677), ('В', 0.039267), ('М', 0.029803), ('Л', 0.029400),
        ('Д', 0.026983), ('Я', 0.026379), ('К', 0.025977), ('П', 0.024768),
        ('З', 0.015908), ('Ы', 0.015707), ('Ь', 0.015103), ('У', 0.013290),
        ('Ч', 0.011679), ('Ж', 0.010673), ('Г', 0.009867), ('Х', 0.008659),
        ('Ф', 0.007249), ('Й', 0.006847), ('Ю', 0.006847), ('Б', 0.006645),
        ('Ц', 0.005034), ('Ш', 0.004229), ('Щ', 0.003625), ('Э', 0.002416),
        ('Ъ', 0.000000)
    ]

    cipher_freq = collections.Counter(cipher_text)
    sorted_cipher_freq = [char for char, _ in cipher_freq.most_common()]

    decryption_key = {}
    for (dec_char, _), enc_char in zip(russian_frequencies, sorted_cipher_freq):
        decryption_key[enc_char] = dec_char

    decoded_text = "".join(decryption_key.get(c, c) for c in cipher_text)

    return decoded_text, decryption_key

with open("cod22.txt", encoding="utf-8") as file:
    encrypted_text = file.read()

decrypted_text, key_mapping = decrypt_cipher(encrypted_text)

with open("decoded_text.txt", "w", encoding="utf-8") as file:
    file.write(decrypted_text)

with open("decryption_key.json", "w", encoding="utf-8") as file:
    json.dump(key_mapping, file, ensure_ascii=False, indent=4)

print("Дешифровка завершена. Файлы сохранены.")
