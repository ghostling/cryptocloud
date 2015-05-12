# Cryptography Final Project
# By Della Anjeh and Jiexi Cao

import os, sys, getopt
import secret
import mimetypes
from azure.storage import BlobService
from azure.http import ( HTTPError, HTTPRequest )
import cryptography.hazmat.backends as b
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

IV_LEN = 12
TAG_LEN = 16
key = open("key.txt","r").read()
container_name = "testcontainer"

blob_service = BlobService(account_name=secret.STORAGE_ACCOUNT_NAME,
        account_key=secret.PRIMARY_ACCESS_KEY)

def main(myopts):
    file_name = ""
    function = ""

    if not myopts:
        print_help_commands()

    # Parses commands given.
    for opt, obj in myopts:
        if opt == "-u":
            file_name = obj
            function = "upload"
        elif opt == "-d":
            file_name = obj
            function = "download"
        elif opt == "-l":
            print "You want to list all the files"
            # TODO: Call option to list all files
        elif opt == "-h":
            print_help_commands()

    if function == "upload":
        print "You want to upload " + file_name
        upload_file(file_name)
    elif function == "download":
        print "You want to download " + file_name
        download_file(file_name)

def print_help_commands():
    # Shows users commands accepted.
    print "\n=== Help Information ===" + \
            "\n -u [filename]  \t Uploads & encrypts specified file." + \
            "\n -d [filename]  \t Downloads & decrypts specified file.\n"

# Note: We wanted to use blob_service.get_blob_to_path(...) originally to
# skip the intermediary step of saving it to a "cipher_out.txt" file, but that
# function is broken in the API.
def download_file(file_name):
    cipher_text = ""
    blob_service.get_blob_to_path(container_name, file_name, 'cipher_out.txt')
    cipher_text = open('cipher_out.txt', 'r').read()
    decrypted = decrypt_file(cipher_text)
    new_file = open("downloaded_"+file_name, "w")
    new_file.write(decrypted)
    new_file.close()

def upload_file(file_name):
    file_type = mimetypes.guess_type(file_name)[0]
    encrypted_file = encrypt_file(file_name)
    blob_service.put_block_blob_from_bytes(
        container_name, file_name, encrypted_file, x_ms_blob_content_type=file_type)

def encrypt_file(file_name):
    iv = os.urandom(IV_LEN)
    file_bytes = open(file_name, "rb").read()
    encryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv),
        backend=b.default_backend()).encryptor()
    cipher_text = encryptor.update(file_bytes) + encryptor.finalize()
    cipher_text = iv + encryptor.tag + cipher_text
    return cipher_text

def decrypt_file(cipher_text):
    iv = cipher_text[:IV_LEN]
    decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, cipher_text[IV_LEN:IV_LEN+TAG_LEN]),
            backend=b.default_backend()).decryptor()
    return decryptor.update(cipher_text[IV_LEN+TAG_LEN:]) + decryptor.finalize()

if __name__ == "__main__":
    myopts, args = getopt.getopt(sys.argv[1:],"u:d:c:l:h")
    main(myopts)

