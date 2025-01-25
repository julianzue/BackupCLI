from colorama import Fore, Style, init
import time
import os
import json


# Set colors and styles

init()

y = Fore.LIGHTYELLOW_EX
r = Fore.LIGHTRED_EX
b = Fore.LIGHTBLUE_EX
c = Fore.LIGHTCYAN_EX
g = Fore.LIGHTGREEN_EX
re = Fore.RESET

dim = Style.DIM
res = Style.RESET_ALL


def create_data_file():
    if not os.path.exists("data.json"):
        with open("data.json", "w") as f:

            data = {
                "path": {
                    "from": [

                    ],
                    "to": [

                    ]
                }
            }

            json.dump(data, f, indent=4)


def set_backup_from():

    print(f"{c}[*] {re}Enter Directory Path")

    with open("data.json", "r") as f:
        data = json.load(f)

    for index, path in enumerate(data["path"]["from"], 1):
        print(f"[{index}] {path}")
    
    backup_from = input(f"{y}[+] From: {re}")

    if backup_from.isnumeric():
        backup_from_path = data["path"]["from"][int(index) - 1]

    else:
        backup_from_path = backup_from

        with open("data.json", "r") as f:
            data = json.load(f)

            if not backup_from in data["path"]["from"]:
                add = input("[+] Add Path to List? [Y|n]: ")

                if add == "" or add == "Y" or add == "y":
                    data["path"]["from"].append(backup_from)

                    with open("data.json", "w") as f:
                        json.dump(data, f, indent=4)

                print(f"{c}[*] {re}Successfully added to list.")

    return backup_from_path
        
    
def set_backup_to():

    print(f"{c}[*] {re}Enter Directory Path")

    with open("data.json", "r") as f:
        data = json.load(f)

    for index, path in enumerate(data["path"]["to"], 1):
        print(f"[{index}] {path}")


    
    backup_to = input(f"{y}[+] To: {re}")

    if backup_to.isnumeric():
        backup_to_path = data["path"]["to"][int(index) - 1]

    else:
        backup_to_path = backup_to

        with open("data.json", "r") as f:
            data = json.load(f)

            if not backup_to in data["path"]["to"]:
                add = input("[+] Add Path to List? [Y|n]: ")

                if add == "" or add == "Y" or add == "y":
                    data["path"]["to"].append(backup_to)

                    with open("data.json", "w") as f:
                        json.dump(data, f, indent=4)

                print(f"{c}[*] {re}Successfully added to list.")

    return backup_to_path


def main():
    create_data_file()

    f = set_backup_from()
    print("")
    t = set_backup_to()

    print("")

    count_of_content = 0

    for dirpath, dirnames, filenames in os.walk(f):
        count_of_content += len(filenames)

    current_count = 0

    count_skipped = 0
    count_copied = 0

    for dirpath, dirnames, filenames in os.walk(f):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        for filename in filenames:

            current_count += 1

            percentage = current_count / count_of_content * 100

            p = "{:3d}".format(int(percentage)) + "%"

            if dirpath.replace(f, "") == "":

                if os.path.exists(f"{t}/{filename}"):
                    count_skipped += 1
                    print(f"{c}[{p}] {dim}{y}[ SKIP ]{re} {'{:04d}'.format(current_count)} {b}{dirpath.replace(f, "")}/{re}{filename}{res}")

                else:
                    count_copied += 1
                    print(f"{c}[{p}] {g}[ COPY ]{re} {'{:04d}'.format(current_count)} {b}{dirpath.replace(f, "")}/{re}{filename}")
                    os.system(f"cp -r '{dirpath}/{filename}' '{t}/{filename}'")
            else:
                if not os.path.exists(f"{t}{dirpath.replace(f, "")}"):
                    os.system(f"mkdir -p '{t}{dirpath.replace(f, "")}'")

                if os.path.exists(f"{t}{dirpath.replace(f, "")}/{filename}"):
                    count_skipped += 1
                    print(f"{c}[{p}] {dim}{y}[ SKIP ]{re} {'{:04d}'.format(current_count)} {b}{dirpath.replace(f, "")}/{re}{filename}{res}")
                else:
                    count_copied += 1
                    print(f"{c}[{p}] {g}[ COPY ]{re} {'{:04d}'.format(current_count)} {b}{dirpath.replace(f, "")}/{re}{filename}")
                    os.system(f"cp -r '{dirpath}/{filename}' '{t}{dirpath.replace(f, "")}/{filename}'")

    print("")
    print(f"{c}[*]{re} Done!")
    print(f"{c}[*]{re} {count_copied} of {count_of_content} files successfully copied.")
    print(f"{c}[*]{re} {count_skipped} of {count_of_content} files skipped (aleady exists).")


main()
