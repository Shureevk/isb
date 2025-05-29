import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as rsa_padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.backends import default_backend


class EncryptionService:
    """Обеспечивает операции шифрования для гибридной криптосистемы."""

    @staticmethod
    def encrypt_key(symmetric_key: bytes, public_key) -> bytes:
        """
        Шифрует симметричный ключ с использованием RSA-OAEP.

        :param symmetric_key: Key to encrypt (16, 24 or 32 bytes)
        :param public_key: RSA public key
        :return: Encrypted key
        :raises Exception: If encryption fails
        """
        try:
            return public_key.encrypt(
                symmetric_key,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise Exception(f"Key encryption failed: {str(e)}")

    @staticmethod
    def decrypt_key(encrypted_key: bytes, private_key: RSAPrivateKey) -> bytes:
        """
        Расшифровывает симметричный ключ с использованием RSA-OAEP.

        :param encrypted_key: Encrypted key to decrypt
        :param private_key: RSA private key
        :return: Decrypted symmetric key
        :raises Exception: If decryption fails
        """
        try:
            return private_key.decrypt(
                encrypted_key,
                rsa_padding.OAEP(
                    mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        except Exception as e:
            raise Exception(f"Key decryption failed: {str(e)}")

    @staticmethod
    def add_padding(data: bytes) -> bytes:
        """
        Добавляет к данным заполнение PKCS7.

        :param data: Data to pad
        :return: Padded data
        :raises Exception: If padding fails
        """
        try:
            padder = sym_padding.PKCS7(64).padder()
            return padder.update(data) + padder.finalize()
        except Exception as e:
            raise Exception(f"Padding failed: {str(e)}")

    @staticmethod
    def encrypt_data(plaintext: bytes, key: bytes) -> tuple[bytes, bytes]:
        """
        Шифрует данные с использованием 3DES-CBC.

        :param plaintext: Data to encrypt
        :param key: Symmetric key (16, 24 or 32 bytes)
        :return: Tuple of (IV, ciphertext)
        """
        try:
            iv = os.urandom(8)

            padder = sym_padding.PKCS7(64).padder()
            padded_data = padder.update(plaintext) + padder.finalize()

            cipher = Cipher(
                algorithms.TripleDES(key),
                modes.CBC(iv),
                backend=default_backend()
            )
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            return iv, ciphertext

        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")