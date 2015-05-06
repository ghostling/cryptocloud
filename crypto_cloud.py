# Cryptography Final Project
# By Della Anjeh and Jiexi Cao

import os, sys, getopt
import secret
import mimetypes
from azure.storage import BlobService
import cryptography.hazmat.backends as b
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

IV_LEN = 12
blob_service = BlobService(account_name=secret.STORAGE_ACCOUNT_NAME,
        account_key=secret.PRIMARY_ACCESS_KEY)
key = open("key.txt","r")

def main(myopts):
    file_name = ""
    container_name = ""
    function = ""

    for opt, obj in myopts:
        if opt == "-u":
            file_name = obj
            function = "upload"
        elif opt == "-d":
            file_name = obj
            function = "download"
        elif opt == "-c":
            container_name = obj
        elif opt == "-l":
            print "You want to list all the files"
            # Call option to list all files
        elif opt == "-h":
            print "-h \t Help Information." + \
                    "\n -u \t Filename of file to upload." + \
                    "\n -c \t Filename of container to add to."
    if function == "upload":
        print "You want to upload %s to container %s" % (file_name, container_name)
        upload_file(file_name, container_name)
    elif function == "download":
        print "You want to download %s to container %s" % (file_name, container_name)
        download_file(file_name, container_name)

def download_file(file_name, container_name):
    cipher_text = ""
    blob_service.get_blob_to_bytes(container_name, file_name, cipher_text)
    decrypted = decrypt_file(cipher_text)
    new_file = open("downloaded_"+file_name, "w")
    new_file.write(decrypted)
    new_file.close()

def upload_file(file_name, container_name):
    if container_name not in blob_service.list_containers():
        blob_service.create_container(container_name)

    file_type = mimetypes.guess_type(file_name)[0]
    encrypted_file = encrypt_file(file_name)
    blob_service.put_block_blob_from_bytes(
        container_name, file_name, encrypted_file, x_ms_blob_content_type=file_type)

def encrypt_file(file_name):
    iv = os.urandom(IV_LEN)
    file_bytes = open(file_name, "rb").read()
    encryptor = Cipher(
        algorithms.AES(key), modes.GCM(iv), backend=b.default_backend()).encryptor()
    cipher_text = iv + encryptor.update(file_bytes) + encryptor.finalize()
    return cipher_text

def decrypt_file(cipher_text):
    iv = cipher_text[:IV_LEN]
    decryptor = Cipher(algorithms.AES(key), modes.GCM(iv), backend=b.default_backend()).decryptor()

    return decryptor.update(cipher_text) + decryptor.finalize()

if __name__ == "__main__":
    myopts, args = getopt.getopt(sys.argv[1:],"u:d:c:l:h")
    main(myopts)

