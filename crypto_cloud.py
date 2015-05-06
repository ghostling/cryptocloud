# Cryptography Final Project
# By Della Anjeh and Jiexi Cao

import os, sys, getopt
import secret
import mimetypes
from azure.storage import BlobService
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

IV_LEN = 12

def main(myopts):
    file_name = ""
    container_name = ""
    for opt, obj in myopts:
        if opt == "-u":
            file_name = obj
        elif opt == "-c":
            container_name = obj
        elif opt == "-l":
            print "You want to list all the files"
            # Call option to list all files
        elif opt == "-h":
            print "-h \t Help Information." + \
                    "\n -u \t Filename of file to upload." + \
                    "\n -c \t Filename of container to add to."
    print "You want to upload %s to container %s" % (file_name, container_name)
    upload_file(file_name, container_name)

def upload_file(file_name, container_name):
    blob_service = BlobService(account_name=secret.STORAGE_ACCOUNT_NAME,
            account_key=secret.PRIMARY_ACCESS_KEY)
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
        algorithms.AES(key), modes.GCM(iv), backend=default_backend()).encryptor()
    ciphertext = iv + encryptor.update(file_bytes) + encryptor.finalize()
    return ciphertext
    
if __name__ == "__main__":
    myopts, args = getopt.getopt(sys.argv[1:],"u:c:l:h")
    main(myopts)
