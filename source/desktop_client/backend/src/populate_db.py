from db_connection import DBConnection
import helpers
import os

USER = "root"
PASSWORD = "1234"
HOST = "127.0.0.1"
DATABASE = "main"

def main():
    db_connection = DBConnection(USER, PASSWORD, HOST, DATABASE)

    path = input("Enter path to song files: ")

    for file in os.listdir(path):
        dir = os.path.join(path, file)
        if os.path.isfile(dir) and file[-3:] == "mp3":
            file_data = helpers.read_file(dir)

            db_connection.write_song(file[:-4], file_data, 1, 1)

    path = input("Enter path to image files: ")
    
    quit = ""

    while quit != "quit":
        id = int(input("Enter song id: "))
        file = input("Enter image name: ")

        dir = os.path.join(path, file)

        ext = file[file.rfind('.') + 1:]

        valid_ext = ["jpg", "jpeg", "webp", "png"]

        if os.path.isfile(dir) and ext in valid_ext:
            file_data = helpers.read_file(dir)

            db_connection.add_image(id, file_data)
        else:
            print("Invalid file")

        quit = input('To quit, enter "quit": ')



if __name__ == "__main__":
    main()