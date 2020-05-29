# -*- coding: utf-8 -*-
import logging
import os
import requests

from tqdm import tqdm
from zipfile import ZipFile


def setup_logging():
    logging.basicConfig(
        format="%(levelname)s - %(asctime)s: %(message)s", datefmt="%H:%M:%S", level=logging.INFO
    )
    return logging.getLogger()


def download_dataset(url, path, block_size=1024):
    r = requests.get(url, allow_redirects=True, stream=True)
    # if we fail then say something
    r.raise_for_status()

    # get total size in bytes.
    total_size = int(r.headers.get("content-length", 0))
    t = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(path, "wb") as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()

    if total_size != 0 and t.n != total_size:
        logger.error("download failure")


def unzip_file(file_name):
    with ZipFile(os.path.join(os.getcwd(), file_name), "r") as zip_ref:
        zip_ref.extractall(os.getcwd())
