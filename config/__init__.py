from os import path as osp
import sys
import yaml


class Config(object):
    def _parse_yaml_error(self, exc):
        print("Error while parsing YAML config file:")
        if hasattr(exc, "problem_mark"):
            if exc.context is not None:
                print(
                    "  parser says\n"
                    + "  {}\n".format(str(exc.problem_mark))
                    + "  {} {}\n".format(exc.problem, exc.context)
                    + "  Please correct data and retry."
                )
            else:
                print(
                    "  parser says\n"
                    + "  {}\n".format(str(exc.problem_mark))
                    + "  {}\n".format(str(exc.problem))
                    + "  Please correct data and retry."
                )
        else:
            print("Something went wrong while parsing yaml file")

    def _read_config(self, filename):
        # print(' * Loading config file {}'.format(filename))
        try:
            with open(filename, "r") as f:
                read_config = yaml.load(f.read(), yaml.SafeLoader)
        except yaml.YAMLError as e:
            self._parse_yaml_error(e)
            raise e
        except IOError as e:
            print("Error while opening config file: {}".format(e))
            raise e
        return read_config

    def __init__(
        self,
        config_dir=osp.dirname(osp.abspath(sys.modules["__main__"].__file__)),
        config_file="config.yml",
        raise_on_fail=True,
    ):
        full_config_file = osp.join(config_dir, config_file)
        if not osp.isfile(full_config_file):
            if raise_on_fail:
                raise ValueError(
                    "config file not found: {}".format(full_config_file)
                )
            else:
                return {}
        self._config = self._read_config(full_config_file)

    def get(self, key, default=None):
        keys = key.split(":")
        search_base = self._config
        for searchkey in keys[:-1]:
            search_base = search_base.get(searchkey, {})
        return search_base.get(keys[-1], default)
