import pyzipper
import subprocess
import concurrent.futures

def zipcracker():
    passwordListPath = input(r"enter password list path: ")
    compressedFilePath = input(r"enter compressed file path: ")
    passwordList = [passwords.strip() for passwords in open(passwordListPath)]
    compressedFile = pyzipper.AESZipFile(compressedFilePath)
    foundPassword = ""
    def tryzippassword(password):
        nonlocal foundPassword
        if foundPassword:
            return
        try:
            compressedFile.extractall(pwd=password.encode())
            foundPassword=password
            if foundPassword != "":
                print(f"Password found!: {foundPassword}")
        except Exception:
            pass
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(tryzippassword, password) for password in passwordList]
    if foundPassword == "":
        print("Password not found in the wordlist!")

def rarcracker():
    passwordListPath = input(r"enter password list path: ")
    compressedFilePath = input(r"enter compressed file path: ")
    passwordList = [passwords.strip() for passwords in open(passwordListPath)]
    foundPassword = ""
    def tryrarpassword(password):
        nonlocal foundPassword
        if foundPassword:
            return
        try:
            result = subprocess.run(["7z", "x", compressedFilePath, f"-p{password}", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                foundPassword = password
                print(f"Password found!: {foundPassword}")
        except Exception:
            pass
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(tryrarpassword, password) for password in passwordList]
    if foundPassword == "":
        print("Password not found in the wordlist!")

print("Welcome to my zip/rar file password cracker!")
while True:
    fileType = input("Choose a file type between zip/rar: ".lower())
    if fileType == "zip":
        zipcracker()
        break
    elif fileType == "rar":
        rarcracker()
        break
    else:
        print(fileType + " is not a supported file type. You may only choose between zip and rar!")