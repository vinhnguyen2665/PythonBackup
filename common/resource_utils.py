import os

from dotenv import load_dotenv

from common import file_utils, gdrive_download
import common.shell_exec as shell

load_dotenv()


def download_third_party_resource(path: str):
    if not file_utils.is_exist(path):
        file_utils.if_not_exist_make_dir(file_utils.get_parent_path(path))
        url = get_resource_url(path)
        gdrive_download.download_file_from_google_drive(url, path)
        out, err = shell.exec("echo " + os.getenv('ROOT_PASSWORD') + " | sudo -S chmod +x " + path)
        print(out)


def get_resource_url(path: str):
    switcher = {
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x64", "mysql.exe"):
            "https://drive.google.com/u/0/uc?id=1AEcAID4tC1nv1hYfPoKhGhVlRWFhATJo&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x64", "mysqldump.exe"):
            "https://drive.google.com/u/0/uc?id=1FAlALHlH0gCgz9QffkRxZQga-siyTG6W&export=download",

        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x32", "mysqldump.exe"):
            "https://drive.google.com/u/0/uc?id=1MLs0PyPgOCCNwt-dZ6JEqPnlyj5ndXLU&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "win_x32", "mysql.exe"):
            "https://drive.google.com/u/0/uc?id=1Vf4Q2yP0x1cLXj9I8XamKpQtrv1eWd_d&export=download",

        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x32", "mysqldump"):
            "https://drive.google.com/u/0/uc?id=1FKzKl_ISQebeNbgU5apsrDklhjtLFbTm&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x32", "mysql"):
            "https://drive.google.com/u/0/uc?id=1tKLENYMsPwWU9iojGSIh-WWMozugUwPY&export=download",

        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysqldump"):
            "https://drive.google.com/u/0/uc?id=1wKR08XGhAEB_CS2yxt1nR0xeJuZ_S0RI&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysql"):
            "https://drive.google.com/u/0/uc?id=1eZGYylpr0ZjeMgol4C-zeWMOoBF0NZG5&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "my_sql", "linux_x64", "mysqld"):
            "https://drive.google.com/u/0/uc?id=10MADyr4h21dC81qshapaVWFQjAEhDCm4&export=download",

        os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "win32-x64", "mongodump.exe"):
            "https://drive.google.com/u/0/uc?id=1eQzjCe6cfVeTvN1p6MEAKYYNw8UNXqgJ&export=download",

        os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "ubuntu_x86_64", "mongodump"):
            "https://drive.google.com/u/0/uc?id=138WLLg7E2t-ZnZGqPsqm1IVm_elpLV0r&export=download",
        os.path.join(file_utils.get_project_root(), "third_party", "mongo_db", "linux_x64", "mongosh"):
            "https://drive.google.com/u/0/uc?id=1SqmTLa71K-Ra1igpivr5kcY9QxyaWrOc&export=download",
    }
    path_exec = switcher.get(path, None)
    return path_exec
