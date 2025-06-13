import os


def delete_user(username):
    os.system(f"rm -rf /home/{username}")
