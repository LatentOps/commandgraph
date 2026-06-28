import os
import subprocess
import venv
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _venv_python(venv_path: Path) -> Path:
    if os.name == 'nt':
        return venv_path / 'Scripts' / 'python.exe'
    return venv_path / 'bin' / 'python'


def _venv_script(venv_path: Path, script_name: str) -> Path:
    if os.name == 'nt':
        return venv_path / 'Scripts' / f'{script_name}.exe'
    return venv_path / 'bin' / script_name


def test_package_install_exposes_cli_entrypoints(tmp_path):
    venv_path = tmp_path / 'venv'
    # Python 3.12+ venvs may omit setuptools; expose the runner build backend
    # while still installing CommandGraph and its console scripts into this venv.
    venv.EnvBuilder(with_pip=True, system_site_packages=True).create(venv_path)
    python = _venv_python(venv_path)

    subprocess.run(
        [
            str(python),
            '-m',
            'pip',
            'install',
            '--no-index',
            '--no-deps',
            '--no-build-isolation',
            '--force-reinstall',
            str(PROJECT_ROOT),
        ],
        check=True,
        cwd=PROJECT_ROOT,
    )

    for script_name in ('commandgraph', 'cmdgraph'):
        result = subprocess.run(
            [str(_venv_script(venv_path, script_name)), '--help'],
            check=True,
            cwd=PROJECT_ROOT,
            text=True,
            capture_output=True,
        )
        assert 'Intent-aware command discovery and safety checks.' in result.stdout
