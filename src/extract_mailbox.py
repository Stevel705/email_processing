# extract mailbox from tar.gz and 
# convert mailbox to eml

# from pathlib import Path
import argparse
import tarfile
import os
from mbox2eml import mbox2eml_from
from pathlib import Path
# traverse root directory, and list directories as dirs and files as files


def main(path):
    
    for fname in Path(path).rglob('*.tar.gz'):
        path_to_extract = str(fname)[:-7]
        if os.path.exists(path_to_extract):
            continue
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=path_to_extract)
        tar.close()
        print(fname)

    for fname_tar in Path(path).rglob('mailbox'):
        mbox2eml_from(fname_tar)

    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='workflow_test')
    parser.add_argument("--path", default=1, help="This is the path to folder with eml or tar.gz")
    args = parser.parse_args()
    path = args.path
    main(path)