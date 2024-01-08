
import importlib
import importlib.util
import os
import sys

from qiskit.providers.aer import Aer


def main():
    if len(sys.argv) < 2:
        path = os.getcwd()
    else:
        path = os.path.abspath(sys.argv[1])
    if os.path.isdir(path):
        path = os.path.join(path, 'main.py')
    assert os.path.exists(path)

    prefix = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'contests'))
    assert path != prefix
    assert os.path.commonpath([prefix, path]) == prefix

    desc = os.path.relpath(path, prefix).split(os.sep)
    contest_id, problem_id = desc[:2]
    module_name = contest_id + '.' + problem_id
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, 'check'):
        backend = Aer.get_backend('aer_simulator')
        if 'GPU' in backend.available_devices():
            backend.set_options(device='GPU')
        assert module.check(Aer.get_backend('aer_simulator'))
    elif hasattr(module, 'solve'):
        print(module.solve())
    else:
        print('No entry point found.')


if __name__ == '__main__':
    main()
