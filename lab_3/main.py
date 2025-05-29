import argparse
import os
import sys
from decryption import DecryptionService
from encryption import EncryptionService
from file_operations import FileOperations
from keygen import SymmetricCrypto, AsymmetricCrypto


def generate_keys(config: dict):
    """
    Генерирует и сохраняет все необходимые криптографические ключи.

    :param config: Configuration dictionary with file paths
    :raises SystemExit: If key generation fails
    """
    print("==== Key Generation Mode ====")

    try:
        key_size = SymmetricCrypto.get_key_size()
        symmetric_key = SymmetricCrypto.generate_key(key_size)
        print(f"Symmetric key ({key_size} bits) generated successfully.")

        private_key, public_key = AsymmetricCrypto.generate_keypair()
        print("RSA keypair (2048 bits) generated successfully.")

        AsymmetricCrypto.save_private_key(private_key, config['private_key'])
        AsymmetricCrypto.save_public_key(public_key, config['public_key'])

        encrypted_key = EncryptionService.encrypt_key(symmetric_key, public_key)
        FileOperations.save_encrypted_key(encrypted_key, config['encrypted_symmetric_key'])

        print("All keys saved successfully!")
    except Exception as e:
        print(f"Key generation error: {str(e)}")
        sys.exit(1)

def encrypt_data(config: dict):
    """
    Шифрует открытый текст с использованием гибридной криптосистемы.

    :param config: Configuration dictionary with file paths
    :raises SystemExit: If encryption fails
    """
    print("==== Encryption Mode ====")
    try:
        encrypted_key = AsymmetricCrypto.load_encrypted_key(config['encrypted_symmetric_key'])
        private_key = AsymmetricCrypto.load_private_key(config['private_key'])
        symmetric_key = EncryptionService.decrypt_key(encrypted_key, private_key)

        plaintext = FileOperations.read_data(config['plaintext'])
        iv, ciphertext = EncryptionService.encrypt_data(plaintext, symmetric_key)

        FileOperations.write_data(config['encrypted_iv'], iv)  # New file for IV
        FileOperations.write_data(config['encrypted_text'], ciphertext)

        print("Data encrypted successfully")
    except Exception as e:
        print(f"Encryption failed: {str(e)}")
        raise SystemExit(1)

def decrypt_data(config: dict) -> None:
    """
    Расшифровывает зашифрованный текст с помощью гибридной криптосистемы.

    :param config: Configuration dictionary with file paths
    :raises SystemExit: If decryption fails
    """
    print("==== Decryption Mode ====")
    try:
        encrypted_key = AsymmetricCrypto.load_encrypted_key(config['encrypted_symmetric_key'])
        private_key = AsymmetricCrypto.load_private_key(config['private_key'])
        symmetric_key = EncryptionService.decrypt_key(encrypted_key, private_key)

        iv = FileOperations.read_data(config['encrypted_iv'])
        ciphertext = FileOperations.read_data(config['encrypted_text'])

        plaintext_bytes = DecryptionService.decrypt_data(ciphertext, symmetric_key, iv)

        try:
            plaintext = plaintext_bytes.decode('utf-8')
        except UnicodeDecodeError:
            plaintext = plaintext_bytes.decode('cp1251')

        FileOperations.write_text_file(config['decrypted_text'], plaintext)

        print("Data decrypted successfully")
    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        raise SystemExit(1)