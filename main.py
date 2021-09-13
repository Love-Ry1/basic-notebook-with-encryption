import datetime
import os
import shutil
from cryptography.fernet import Fernet


def create_notebook():      # Creates a notebook (folder)
    name = input("Title of notebook: ")

    try:
        os.mkdir(name)
    except OSError:
        print(f"Failed to create the notebook: {name}")
    else:
        print(f"Sucessfully created the notebook: {name}")


def delete_notebook():              # Deletes a notebook (folder)
    notebook_list = os.listdir()
    print("Number of notebooks: ", len(notebook_list))
    for x in range(len(notebook_list)):                     # Lists available notebooks
        print(f"{x+1}: {notebook_list[x]}")

    name = input("Title of the notebook you want to delete: ")

    try:
        if name.isnumeric() and 0 < int(name) <= len(notebook_list):    # Deletes the correct notebook if
            shutil.rmtree(notebook_list[int(name) - 1])                 # the input is a number
        else:
            shutil.rmtree(name)                                         # Deletes correct notebook if input is the name
    except OSError:
        print("Could not delete notebook: ", name)
    else:
        print("Successfully deleted notebook: ", name)


def open_notebook():        # Opens a notebook (folder)
    notebook_list = os.listdir()
    cwd = os.getcwd()
    print("Number of notebooks: ", len(notebook_list))
    for x in range(len(notebook_list)):
        print(f"{x+1}: {notebook_list[x]}")

    name = input("Number/Name of notebook: ")
    if name.isnumeric() and 0 < int(name) <= len(notebook_list):
        os.chdir(notebook_list[int(name) - 1])
    elif os.path.exists(name):
        os.chdir(name)
    else:
        print("The notebook does not exist.")
        return

    notes_list = os.listdir()
    print("Number of notes: ", len(notes_list))
    for notes in notes_list:        # Displays the notes in the current notebook
        print(notes)

    while True:                     # Displays the options in the current notebook
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


def add_note():     # Takes user input as a string and saves it to a note (.txt file)
    title = input("Title of note: ")
    user_input = input("Write your text: ")
    filename = title.replace(" ", "") + ".txt"
    note = open(filename, "a")
    note.write(str(datetime.datetime.now()) + "\n")     # Marks the note with the current date and time
    note.write(title + "\n")

    characters = 0
    for i in range(0, len(user_input)):                 # After every 40 characters it makes a linebreak instead
        if user_input[i] == " " and characters >= 40:   # of a space.
            note.write('\n')
            characters = 0
        else:
            note.write(user_input[i])
            characters += 1

    note.close()


def delete_note():
    notes_list = os.listdir()
    for x in range(len(notes_list)):
        print(f"{x+1}: {notes_list[x]}")

    filename = input("Name of note you want to delete: ")
    if filename.isnumeric() and 0 < int(filename) <= len(notes_list):
        os.remove(notes_list[int(filename) - 1])
    elif os.path.exists(filename):
        os.remove(filename)
    else:
        print("The note does note exist.")
        return

    print(f"Sucessfully deleted {filename}")


def read_note():
    notes_list = os.listdir()
    for x in range(len(notes_list)):
        print(f"{x+1}: {notes_list[x]}")

    name = input("Note to read: ")
    if name.isnumeric() and 0 < int(name) <= len(notes_list):
        note = open(notes_list[int(name) - 1], 'r')
    elif os.path.exists(name):
        note = open(name, 'r')
    else:
        print("The note does not exist.")
        return
    print(note.read())


def gen_key():
    key = Fernet.generate_key()                 # Generates a new encryption key
    answer = input(f"Your key is: {key.decode()}\nDo you want to save it (y/n)?")
    if answer == "y":
        with open("key.key", "wb") as key_file:     # Saves it to a file
            key_file.write(key)


def load_key():     # Loads a saved en/decryption key or gives the option to generate a new one
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
    notes_list = os.listdir()
    for x in range(len(notes_list)):
        print(f"{x+1}: {notes_list[x]}")

    title = input("Note to encrypt: ")
    if title.isnumeric() and 0 < int(title) <= len(notes_list):
        title = notes_list[int(title) - 1]

    with open(title, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(title, "wb") as file:
        file.write(encrypted_data)


def decrypt_note():
    key = load_key()
    f = Fernet(key)
    notes_list = os.listdir()
    for x in range(len(notes_list)):
        print(f"{x+1}: {notes_list[x]}")

    title = input("Note to decrypt: ")
    if title.isnumeric() and 0 < int(title) <= len(notes_list):
        title = notes_list[int(title) - 1]

    with open(title, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(title, "wb") as file:
        file.write(decrypted_data)


def init():                                 # Initialization func. Creates the folder "Notebooks" if it doesn't exist
    if not os.path.exists('Notebooks'):     # and changes working dir to the folder.
        os.makedirs('Notebooks')

    os.chdir('Notebooks')


def options():  # Shows notebook options.
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


def main():
    init()
    while True:
        options()


if __name__ == "__main__":
    main()


# TODO:
# Improve load_key func (not possible to enter invalid key, possible to exit the func)
# Solution to if you add a note/notebook that already exists.
# Command to list available notes.
# Improve the cryptography (save different keys etc.)
# Add success/error messages
# Find/fix bugs
# Code optimization
