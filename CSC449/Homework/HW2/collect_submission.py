"""This program collects your submission and generates a zip file. To submit
your homework, please run this program and upload the generated zip file to
Blackboard.

"""

import os
import zipfile
import argparse


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


parser = argparse.ArgumentParser(
    description="Collect your homework submission.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    "--coding_framework",
    default="code/",
    help="a folder that contains the implemented framework"
)
parser.add_argument(
    "--homework",
    default="homework.pdf",
    help="the written part of the homework"
)
parser.add_argument(
    "--submission",
    default="homework.zip",
    help="the generated zip file for submission"
)
args = parser.parse_args()

assert os.path.isdir(args.coding_framework), \
    "{} not found!".format(args.coding_framework)
assert os.path.isfile(args.homework), \
    "{} not found!".format(args.homework)

zip_ref = zipfile.ZipFile(args.submission, mode='w')
zipdir(args.coding_framework, zip_ref)
zip_ref.write(args.homework)
zip_ref.close
