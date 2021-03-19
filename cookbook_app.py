import yaml


def loadConfig(file_path):
    """Returns config dict object from given filepath"""
    try:
        with open(file_path, "r") as cfg_file:
            cfg = yaml.safe_load(cfg_file)
    except Exception as e:
        print("Could not find file path: " + file_path)
    else:
        print("*** Config file found. ***")
        return cfg




if __name__ == "__main__":
    pass