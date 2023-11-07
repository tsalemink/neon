import argparse
import os
import platform

import PySide6 as RefMod

import PyInstaller.__main__

from cmapps.neon.settings.mainsettings import APPLICATION_NAME


# Set Python optimisations on.
os.environ['PYTHONOPTIMIZE'] = '1'

here = os.path.dirname(__file__)


def main():
    run_command = [
        '../../src/cmapps/neon/neon.py',
        '-n', f'{APPLICATION_NAME}',
        '--windowed',
        '--noconfirm',
    ]

    pyside_dir = os.path.dirname(RefMod.__file__)

    if platform.system() == 'Darwin':
        rcc_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "rcc")
        uic_exe = os.path.join(pyside_dir, 'Qt', 'libexec', "uic")

        macos_icon = os.path.join('..', 'macos', 'Neon.icns')
        run_command.append(f'--icon={macos_icon}')

    elif platform.system() == "Windows":
        rcc_exe = os.path.join(pyside_dir, "rcc.exe")
        uic_exe = os.path.join(pyside_dir, "uic.exe")

        win_icon = os.path.join('..', 'win', 'Neon.ico')
        run_command.append(f'--icon={win_icon}')

    else:
        raise NotImplementedError("Platform is not supported for creating a Neon application.")

    run_command.append(os.pathsep.join([f'--add-binary={rcc_exe}', 'PySide6/']))
    run_command.append(os.pathsep.join([f'--add-binary={uic_exe}', 'PySide6/']))

    print('Running command: ', run_command)
    PyInstaller.__main__.run(run_command)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="create_application")
    args = parser.parse_args()

    main()
