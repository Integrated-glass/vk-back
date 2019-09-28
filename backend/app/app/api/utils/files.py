import os


def create_dir_if_not_exists(path: str):
  if not os.path.exists(path):
    os.makedirs(path)
