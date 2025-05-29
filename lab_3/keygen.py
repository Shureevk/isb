import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.exceptions import UnsupportedAlgorithm


class SymmetricCrypto:
    """Генерация симметричных ключей для 3DES."""

    @staticmethod
    def get_key_size() -> int:
        """
        Prompts and validates the key size.

        :return: The size of the key in bits (64, 128, or 192).
        :raises ValueError: If the input is not an integer or not one of the allowed sizes.
        """
        while True:
            try:
                size = int(input("Enter key length (64, 128, or 192 bits): "))
                if size not in [64, 128, 192]:
                    print("Error: Allowed sizes are 64, 128, or 192 bits!")
                else:
                    return size
            except ValueError:
                print("Error: Please enter an integer!")

    @staticmethod
    def generate_key(key_size: int) -> bytes:
        """
        Генерирует случайный симметричный ключ.

        :param key_size: The size of the key in bits (must be 64, 128, or 192).
        :return: A byte string representing the generated key.
        :raises Exception: If an error occurs during key generation.
        """
        try:
            return os.urandom(key_size // 8)
        except Exception as e:
            raise Exception(f"Error generating key: {str(e)}")


class AsymmetricCrypto:
    """Операции с асимметричными ключами RSA."""

    @staticmethod
    def generate_keypair() -> tuple:
        """
        Генерирует пару ключей RSA.

        :return: A tuple containing the private key and the public key.
        :raises Exception: If an error occurs during key pair generation.
        """
        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            return private_key, private_key.public_key()
        except Exception as e:
            raise Exception(f"Error generating keys: {str(e)}")

    @staticmethod
    def save_private_key(private_key: RSAPrivateKey, filename: str) -> None:
        """
        Сохраняет закрытый ключ в файл.

        :param private_key: The RSA private key to save.
        :param filename: The path to the file where the key will be saved.
        :raises Exception: If an error occurs while saving the private key.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            with open(filename, "w") as f:
                f.write(pem.decode('utf-8'))
        except Exception as e:
            raise Exception(f"Error saving private key: {str(e)}")

    @staticmethod
    def save_public_key(public_key, filename: str) -> None:
        """
        Сохраняет открытый ключ в файл.

        :param public_key: The RSA public key to save.
        :param filename: The path to the file where the key will be saved.
        :raises Exception: If an error occurs while saving the public key.
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            with open(filename, "w") as f:
                f.write(pem.decode('utf-8'))
        except Exception as e:
            raise Exception(f"Error saving public key: {str(e)}")

    @staticmethod
    def load_private_key(path: str) -> RSAPrivateKey:
        """
        Загружает закрытый ключ из файла.

        :param path: The path to the file containing the private key.
        :return: The loaded RSA private key.
        :raises UnsupportedAlgorithm: If the key algorithm is not supported.
        :raises ValueError: If the key format is invalid.
        :raises Exception: If an error occurs while loading the key.
        """
        try:
            with open(path, "r") as f:
                pem = f.read().encode('utf-8')
            return serialization.load_pem_private_key(
                pem,
                password=None,
                backend=default_backend()
            )
        except UnsupportedAlgorithm:
            raise Exception("Unsupported key algorithm")
        except ValueError:
            raise Exception("Invalid key format")
        except Exception as e:
            raise Exception(f"Error loading key: {str(e)}")

    @staticmethod
    def load_encrypted_key(path: str) -> bytes:
        """
        Загружает зашифрованный ключ из файла.

        :param path: The path to the file containing the encrypted key.
        :return: The loaded encrypted key in bytes.
        :raises Exception: If an error occurs while loading the key.
        """
        try:
            with open(path, "rb") as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error loading key: {str(e)}")