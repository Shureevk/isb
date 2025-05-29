from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


class DecryptionService:
    """Обеспечивает операции дешифрования для гибридной криптосистемы."""

    @staticmethod
    def remove_padding(padded_data: bytes) -> bytes:
        """
        Удаляет заполнение PKCS7 из расшифрованных данных.

        :param padded_data: Data with padding
        :return: Original unpadded data
        :raises ValueError: If padding is invalid
        """
        try:
            unpadder = sym_padding.PKCS7(64).unpadder()
            return unpadder.update(padded_data) + unpadder.finalize()
        except ValueError as e:
            raise ValueError(f"Padding removal error: {str(e)}")

    @staticmethod
    def decrypt_data(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Расшифровывает данные с помощью 3DES-CBC.

        :param ciphertext: Data to decrypt
        :param key: Symmetric key
        :param iv: Initialization vector used for encryption
        :return: Decrypted plaintext
        """
        try:
            cipher = Cipher(
                algorithms.TripleDES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = sym_padding.PKCS7(64).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

            return plaintext

        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")