import datetime
import os
import shutil
from cryptography.fernet import Fernet


def create_notebook():
    name = input("Title of notebook: ")

    try:
        os.mkdir(name)
    except OSError:
        print(f"Failed to create the notebook: {name}")
    else:
        print(f"Sucessfully created the notebook: {name}")


def delete_notebook():
    title = input("Title of the notebook you want to delete: ")
    cwd = os.getcwd()
    path = cwd + "/" + title
    try:
        shutil.rmtree(path)
    except OSError:
        print("Could not delete notebook: ", title)
    else:
        print("Successfully deleted notebook: ", title)


def open_notebook():
    notebook_list = os.listdir()
    cwd = os.getcwd()
    print("Number of notebooks: ", len(notebook_list))
    for notebook in notebook_list:
        print(notebook)

    name = input("Name of notebook: ")
    if os.path.exists(name):
        os.chdir(name)
    else:
        print("The notebook does not exist.")
        return

    notes_list = os.listdir()
    print("Number of notes: ", len(notes_list))
    for notes in notes_list:
        print(notes)

    while True:
        print("Options:\n"
              "1. Create a note\n"
              "2. Read a note\n"
              "3. Encrypt a note\n"
              "4. Decrypt a note\n"
              "5. Generate a key\n"
              "6. Delete a note\n"
              "7. Go back\n")
        option = input("Your choice: ")
        if option == "1":
            add_note()
        if option == "2":
            read_note()
        if option == "3":
            encrypt_note()
        if option == "4":
            decrypt_note()
        if option == "5":
            gen_key()
        if option == "6":
            delete_note()
        if option == "7":
            os.chdir(cwd)
            return


def add_note():
    title = input("Title of note: ")
    user_input = input("Write your text: ")
    filename = title.replace(" ", "") + ".txt"
    note = open(filename, "a")
    note.write(str(datetime.datetime.now()) + "\n")
    note.write(title + "\n")

    characters = 0
    for i in range(0, len(user_input)):
        if user_input[i] == " " and characters >= 40:
            note.write('\n')
            characters = 0
        else:
            note.write(user_input[i])
            characters += 1

    note.close()


def delete_note():
    filename = input("Name of note you want to delete: ") + '.txt'
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Sucessfully deleted {filename}")
    else:
        print("The note does note exist.")
        return


def read_note():
    title = input("Note to read: ") + '.txt'
    if os.path.exists(title):
        note = open(title, "r")
        print(note.read())
    else:
        print("The note does not exist.")
        return


def gen_key():
    key = Fernet.generate_key()
    answer = input(f"Your key is: {key.decode()}\nDo you want to save it (y/n)?")
    if answer == "y":
        with open("key.key", "wb") as key_file:
            key_file.write(key)


def load_key():
    while True:
        answer = input("Do you want to load the saved key (y/n)? ")
        if answer == "y":
            try:
                key = open("key.key", "rb").read()
                break
            except Exception:
                ans = input("There is no saved key. Do you want to generate one (y/n)? ")
                if ans == "y":
                    gen_key()
                if ans == "n":
                    continue
        elif answer == "n":
            key = input("Enter the key: ")
            key = key.encode()
            break
    print(key.decode())
    return key


def encrypt_note():
    key = load_key()
    f = Fernet(key)
    title = input("Note to encrypt: ")
    filename = title + ".txt"
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)


def decrypt_note():
    key = load_key()
    f = Fernet(key)
    title = input("Note to decrypt: ")
    filename = title + ".txt"
    with open(filename, "rb") as file:
        encrypted_data = file.read()

    decrypted_data = f.decrypt(encrypted_data)

    with open(filename, "wb") as file:
        file.write(decrypted_data)


def init():
    if not os.path.exists('Notebooks'):
        os.makedirs('Notebooks')

    os.chdir('Notebooks')


def options():
    while True:
        print("Options:\n"
              "1. Create a notebook\n"
              "2. Open a notebook\n"
              "3. Delete a notebook\n")
        option = input("Your choice: ")
        if option == "1":
            create_notebook()
        elif option == "2":
            open_notebook()
        elif option == "3":
            delete_notebook()
        else:
            print("Answer with a number between 1 and 3\n")


init()
while True:
    options()

# TODO:
# Add comments to the code.
# Solution to if you add a note/notebook that already exists.
# Command to list available notes.
# Improve the cryptography (save different keys etc.)
# Not needing to write whole note/notebook name.
# Find/fix bugs
# Code optimization
