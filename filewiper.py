import os
import random
import shutil
from cryptography.fernet import Fernet
import time


class SecureDeleter:
    def __init__(self, path):
        self.path = path

    def overwrite_file(self, file_path, passes=7):
        writes = 0
        """Overwrites the file with multiple patterns and random data."""
        patterns = [b"\x00", b"\xff", random.randbytes(1)]
        length = os.path.getsize(file_path)
        for _ in range(passes):
            with open(file_path, "r+b") as file:
                for pattern in patterns:
                    print(f"Written{writes}")
                    writes += 1
                    file.seek(0)
                    for _ in range(length):
                        file.write(pattern)
                # Final pass with random data for each byte
                file.seek(0)
                file.write(random.randbytes(length))

    def delete_file(self, file_path):
        """Securely deletes a file."""
        if os.path.isfile(file_path):
            self.overwrite_file(file_path)
            os.remove(file_path)

    # Look here for folder decrypt and encrypt
    def delete_folder(self, folder_path):
        """Securely deletes a folder and its contents."""
        key = Fernet.generate_key()
        fernet = Fernet(key)
        if os.path.isdir(folder_path):
            for root, dirs, files in os.walk(folder_path, topdown=False):
                for name in files:
                    file_path = os.path.join(root, name)
                    try:
                        # Read the original file contents
                        with open(file_path, "rb") as file:
                            original_data = file.read()

                        # Encrypt the file contents
                        encrypted_data = fernet.encrypt(original_data)

                        # Overwrite the file with encrypted data
                        with open(file_path, "wb") as file:
                            file.write(encrypted_data)

                        # Securely delete the file
                        self.delete_file(file_path)
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")

                # Remove empty directories
                for name in dirs:
                    dir_path = os.path.join(root, name)
                    try:
                        os.rmdir(dir_path)
                    except Exception as e:
                        print(f"Error removing directory {dir_path}: {e}")

            # Finally remove the root folder
            shutil.rmtree(folder_path)

    # def wipe_free_space(self, drive, size=1024*1024*10): # 10MB default file size
    #     """Writes temporary files with random data to overwrite free disk space."""
    #     temp_files = []
    #     try:
    #         while True:
    #             temp_file = os.path.join(drive, f"temp_{random.randint(0, 999999)}.dat")
    #             with open(temp_file, "wb") as file:
    #                 file.write(random.randbytes(size))
    #             temp_files.append(temp_file)
    #     except OSError:  # Typically disk full
    #         for temp_file in temp_files:
    #             os.remove(temp_file)

    def execute(self):
        """Determines whether the path is a file or folder and deletes it securely."""
        if os.path.isfile(self.path):
            self.delete_file(self.path)
        elif os.path.isdir(self.path):
            self.delete_folder(self.path)
        else:
            print("Path does not exist.")


# user_path = input("Please enter the path to the file: \n")


def check_path_type(path) -> str:
    if os.path.isdir(path):
        return "Directory"
    elif os.path.isfile(path):
        return "File"
    else:
        return "Invalid path"


def func(user_path):
    result_tuple = check_path_type(user_path)
    if result_tuple == "File":
        # Encrypts file DOES NOT SAVE KEY
        key = Fernet.generate_key()
        fernet = Fernet(key)
        with open(user_path, "rb") as file:
            original_data = file.read()

        encrypted_data = fernet.encrypt(original_data)

        with open(user_path, "wb") as file:
            file.write(encrypted_data)
        print("File encrypted successfully. Key discarded, no decryption possible.")

    elif result_tuple == "Folder":
        try:
            # Generate a random encryption key (not saved)
            key = Fernet.generate_key()
            fernet = Fernet(key)

            # Walk through the directory recursively
            for root, dirs, files in os.walk(user_path):
                for file_name in files:
                    file_path = os.path.join(root, file_name)

                    # Encrypt each file
                    try:
                        with open(file_path, "rb") as file:
                            original_data = file.read()

                        # Encrypt the data
                        encrypted_data = fernet.encrypt(original_data)

                        # Overwrite the file with encrypted data
                        with open(file_path, "wb") as file:
                            file.write(encrypted_data)

                        print(f"Encrypted: {file_path}")

                    except Exception as e:
                        print(f"Failed to encrypt {file_path}: {e}")

            # Discard the key
            print(
                "Folder encrypted successfully. Key discarded, no decryption possible."
            )

        except FileNotFoundError:
            print(f"Error: Folder '{user_path}' not found.")
        except PermissionError:
            print(f"Error: Permission denied when accessing '{user_path}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# deleter = SecureDeleter(
#     r"C:\Users\blast\github-classroom\Cybersecurity\cyber_project\file.txt"
# )

# deleter = SecureDeleter(
#     r"/mnt/c/Users/blast/github-classroom/Cybersecurity/cyber_project/file.txt"
# )


def main():
    print(
        "Welcome to the file deleter. This program will overwrite and encrypt the contents in a file. RECOVERY IS NOT POSSIBLE"
    )
    print(
        "By typing yes you are aware that the contents will be deleted and can not be recovered"
    )
    usr_input = input("Type yes if you are aware:")
    if usr_input.lower() == "yes":
        user_path = input("Please enter the path to the file: \n")
        time_start = time.time()
        encrypt_stuff = func(user_path)
        deleter = SecureDeleter(user_path)
        deleter.execute()
        time_end = time.time()
        elapsed_time = time_end - time_start
        hours, rem = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(rem, 60)
        milliseconds = (seconds % 1) * 1000
        print(
            f"It took, {int(hours)}h {int(minutes)}m {int(seconds)}s {int(milliseconds)}ms"
        )
    elif usr_input.lower() == "no":
        print("closing program")
    else:
        print("enter yes or no")


main()
# def main():
#     print(
#         "Welcome to the file deleter. This program will overwrite and encrypt the contents in a file. RECOVERY IS NOT POSSIBLE"
#     )
#     user_path = input("Please enter the path to the file: \n")
#     deleter.execute()
#     print("File has been deleted.")


# main()
