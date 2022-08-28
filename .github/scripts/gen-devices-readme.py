import re
import os
import json
import github

try:
    GH_TOKEN = os.environ.get("GH_TOKEN")
except Exception:
    print("GH_TOKEN missing")
    exit(0)
START_COMMENT = "<!--START_SECTION:devices-->"
END_COMMENT = "<!--END_SECTION:devices-->"
RE_PATTERN = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"
jsonDir = "builds"

XIAOMI = []
REALME = []
SAMSUNG = []
ASUS = []
ONEPLUS = []
LENOVO = []
NOKIA = []
MEIZU = []
OTHER = []

def generate_new_readme(devices, readme):
    replace_readme = f"{START_COMMENT}\n{devices}\n{END_COMMENT}"
    return re.sub(RE_PATTERN, replace_readme, readme)

def get_all_filenames():
    FILENAMES = []
    for device in os.listdir(jsonDir):
        FILENAMES.append(device.replace(".json", ""))
    return FILENAMES

def get_info(filename):
    with open(f"{jsonDir}/{filename}.json") as device_file:
            info = json.loads(device_file.read())
            CODENAME = info['device']
            DEVICE_NAME = info['device_name']
            MAINTAINER = info['tg_username']
    return {
        "codename": CODENAME,
        "device_name": DEVICE_NAME,
        "maintainer": MAINTAINER
    }

def check_and_add_device(filename):
    info = get_info(filename)
    device_name = info['device_name']
    if device_name.upper().find("XIAOMI") != -1 or device_name.upper().find("REDMI") != -1 or device_name.upper().find("POCO") != -1 or device_name.upper().find("MI") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        XIAOMI.append(TEXT)
    elif device_name.upper().find("REALME") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        REALME.append(TEXT)
    elif device_name.upper().find("SAMSUNG") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        SAMSUNG.append(TEXT)
    elif device_name.upper().find("ASUS") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        ASUS.append(TEXT)
    elif device_name.upper().find("ONEPLUS") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        ONEPLUS.append(TEXT)
    elif device_name.upper().find("LENOVO") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        LENOVO.append(TEXT)
    elif device_name.upper().find("NOKIA") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        NOKIA.append(TEXT)
    elif device_name.upper().find("MEIZU") != -1:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        MEIZU.append(TEXT)
    else:
        TEXT = f"{device_name} ({info['codename']}) by {info['maintainer']}"
        OTHER.append(TEXT)

def list_devices(device_list):
    TEXT = "```\n"
    for device in device_list:
        TEXT += f"{device}\n"
    TEXT += "```"
    return TEXT

def update_devices():
    for filename in get_all_filenames():
        check_and_add_device(filename)
    UPDATE = ""
    UPDATE += "## - Xiaomi Devices\n"
    UPDATE += f"{list_devices(sorted(XIAOMI))}\n\n"
    UPDATE += "## - Realme Devices\n"
    UPDATE += f"{list_devices(sorted(REALME))}\n\n"
    UPDATE += "## - Samsung Devices\n"
    UPDATE += f"{list_devices(sorted(SAMSUNG))}\n\n"
    UPDATE += "## - Asus Devices\n"
    UPDATE += f"{list_devices(sorted(ASUS))}\n\n"
    UPDATE += "## - OnePlus Devices\n"
    UPDATE += f"{list_devices(sorted(ONEPLUS))}\n\n"
    UPDATE += "## - Lenovo Devices\n"
    UPDATE += f"{list_devices(sorted(LENOVO))}\n\n"
    UPDATE += "## - Nokia Devices\n"
    UPDATE += f"{list_devices(sorted(NOKIA))}\n\n"
    UPDATE += "## - Meizu Devices\n"
    UPDATE += f"{list_devices(sorted(MEIZU))}\n\n"
    UPDATE += "## - Other Devices\n"
    UPDATE += f"{list_devices(sorted(OTHER))}"
    UPDATE += ""
    return UPDATE

try:
    g = github.Github(GH_TOKEN)
    committer = github.InputGitAuthor("TheElixirRobot", "projectelixirbot@gmail.com")
    repo = g.get_repo("ProjectElixir-Devices/official_devices")
    commit_message = "Elixir: Update devices readme [BOT]"
    contents = repo.get_readme()
    readme = contents.decoded_content.decode()
    device_update = update_devices()
    new_readme = generate_new_readme(device_update, readme)
    if new_readme != readme:
        repo.update_file(
            path=contents.path,
            message=commit_message,
            content=new_readme,
            sha=contents.sha,
            branch='A13',
            committer=committer
        )
    else:
        print("Nothing to change in devices readme\nExitting...")
        exit(1)
except Exception as e:
    print(f"Exception Occurred: {str(e)}")
