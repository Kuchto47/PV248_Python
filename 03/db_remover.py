# Personal script to automatically remove db if there is some so
# I don't have to do it every time before running import script.
# No risk for actual solution, because this script is only run
# as a pre-step of import script in pycharm configuration :)
import os


def remove_db_if_exists():
    db_name = "scorelib.dat"
    if os.path.exists(db_name):
        os.remove(db_name)


remove_db_if_exists()
