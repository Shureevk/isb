import json
import os


class FileOperations:
    """Обеспечивает файловые операции для гибридной криптосистемы."""

    @staticmethod
    def save_encrypted_key(encrypted_key: bytes, path: str) -> None:
        """
        Saves the encrypted key to a file.

        :param encrypted_key: The encrypted key in bytes
        :param path: The path to the file where the key will be saved
        :raises Exception: If an error occurs while saving the key
        """
        try:
            with open(path, "wb") as file:
                file.write(encrypted_key)
        except IOError as e:
            raise Exception(f"Error saving key: {str(e)}")

    @staticmethod
    def read_data(filename: str) -> bytes:
        """
        Считывает данные из файла.

        :param filename: The name of the file to read from
        :return: Data read from the file in bytes
        :raises Exception: If the file is not found or an error occurs during reading
        """
        try:
            with open(filename, "rb") as file:
                return file.read()
        except FileNotFoundError:
            raise Exception(f"File not found: {filename}")
        except IOError as e:
            raise Exception(f"Error reading file: {str(e)}")

    @staticmethod
    def write_data(filename: str, data: bytes) -> None:
        """
        Записывает данные в файл.

        :param filename: The name of the file to write to
        :param data: The data in bytes to write
        :raises Exception: If an error occurs during writing
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'wb') as f:
                f.write(data)
        except IOError as e:
            raise Exception(f"Error writing file: {str(e)}")

    @staticmethod
    def write_text_file(filename: str, text: str) -> None:
        """
        Записывает текст в файл с кодировкой UTF-8 BOM.

        :param filename: The name of the file to write to
        :param text: The text content to write
        :raises Exception: If an error occurs during writing
        """
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8-sig') as f:
                f.write(text)
        except Exception as e:
            raise Exception(f"Text file write error: {str(e)}")

    @staticmethod
    def load_config(filename: str) -> dict:
        """
        Загружает конфигурацию из файла JSON.

        :param filename: The name of the JSON configuration file
        :return: A dictionary containing the loaded configuration
        :raises Exception: If the file is not found, JSON format is invalid, or another error occurs
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found: {filename}")
        except json.JSONDecodeError:
            raise Exception(f"JSON format error in file: {filename}")
        except Exception as e:
            raise Exception(f"Error loading configuration: {str(e)}")