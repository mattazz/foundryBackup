import zipfile
import utils
import os

## THIS ONLY UNZIPS IN THE MAC FILE DIRECTORY
## NOT WINDOWS YET


def unzipBackup(
    file_name="foundry_backup_2024-02-13_23-01-24.zip", folder_name="FoundryVTT"
):
    """_summary_
    Unzips the FoundryVTT Folder.

    Args:
        file_name (str, optional): _description_. Defaults to "foundry_backup_2024-02-13_23-01-24.zip".
        folder_name (str, optional): _description_. Defaults to "FoundryVTT".
    """

    foundry_path = os.path.expanduser("~/Library/Application Support/")

    # Unzips the file
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(foundry_path)

    utils.print_hash(40)
    print(f"File {file_name} unzipped at: {foundry_path}")
    utils.print_hash(40)

    # Folder is FoundryVTT, the contents inside is the one you want to access and copy


unzipBackup()
