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