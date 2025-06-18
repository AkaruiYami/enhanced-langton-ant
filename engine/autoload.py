import pathlib
from importlib import util


def load_py_files(directory):
    path = pathlib.Path(directory)
    for file in path.glob("*.py"):
        module_name = file.stem
        module_path = file.absolute()
        spec = util.spec_from_file_location(module_name, module_path)
        if spec is None:
            print(f"Skipping {module_name} since loader can't construct spec from it.")
            continue
        module = util.module_from_spec(spec)
        loader = spec.loader
        if loader is None:
            print(f"Cannot load {module_name} due unable to get the spec.loader.")
            continue
        loader.exec_module(module)
        print(f"Module loaded: {module_name}")
