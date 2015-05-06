# Cryptography Final Project
# By Della Anjeh and Jiexi Cao

import os, sys, getopt
import secret
from azure.storage import BlobService

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
    blob_service.create_container(container_name)

if __name__ == "__main__":
    myopts, args = getopt.getopt(sys.argv[1:],"u:c:l:h")
    main(myopts)
