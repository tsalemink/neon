#!/usr/bin/env python
import argparse
import glob
import os
import os.path
import platform
import subprocess
import sys


NEON_REPO = "neon"

here = os.path.abspath(os.path.dirname(__file__))


def main():
    parser = argparse.ArgumentParser(prog="release_preparation")
    parser.add_argument("neon_release", help="tag from neon codebase")
    parser.add_argument('-l', '--local', help='absolute path to locally available Neon')
    parser.add_argument("--pre", action='store_true', help="Allow pre-release versions")
    args = parser.parse_args()

    cut_short = False
    local_neon = args.local

    available_pips = glob.glob(os.path.join(os.path.dirname(sys.executable), 'pip*'))
    if len(available_pips) == 0:
        sys.exit(1)

    pip = available_pips[0]

    result = subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print(' == result install:', result.returncode, flush=True)

    # Always install numpy.
    result = subprocess.run([pip, "install", "numpy"])
    print(' == result install extras:', result.returncode, flush=True)

    # TODO: Maybe remove this block...?
    if local_neon is None:

        # TODO: REMOVE:
        print("NO LOCAL...")

        neon_url = f"https://github.com/cmlibs/{NEON_REPO}"
        local_neon = NEON_REPO
        result = subprocess.run(["git", "-c", "advice.detachedHead=false", "clone", "--depth", "1", neon_url, "-b", args.neon_release])
        print(' == result git:', result.returncode, flush=True)

    result = subprocess.run([pip, "install", "-e", f"{local_neon}/src"])
    print(' == result install:', result.returncode, flush=True)

    working_env = os.environ.copy()

    if cut_short:
        return

    current_directory = os.getcwd()

    # TODO: REMOVE:
    #   This is already in the repository; "res" is listed as one of the
    # print("START...")
    # directory_contents = os.listdir(current_directory)
    # for entry in directory_contents:
    #     print(entry)

    # TODO: REMOVE:
    # print("AND...")
    # os.chdir(f"{NEON_REPO}")
    # directory_contents = os.listdir(os.getcwd())
    # for entry in directory_contents:
    #     print(entry)
    # print("END...")

    # TODO: Correct path...
    # os.chdir(f"{NEON_REPO}/res/pyinstaller/")
    os.chdir(f"res/pyinstaller/")

    result = subprocess.run([sys.executable, "create_application.py"], env=working_env)
    print(' == result application creation:', result.returncode, flush=True)
    os.chdir(current_directory)
    if result.returncode:
        sys.exit(result.returncode)

    # Define a release name from the release tag
    tag = args.neon_release
    tag_parts = tag[1:].split('.')
    release_name = '.'.join(tag_parts[:3])

    if platform.system() == "Windows":
        # TODO: Correct path...
        # os.chdir(f"{NEON_REPO}/res/win")
        os.chdir(f"res/win")
        result = subprocess.run([sys.executable, "create_installer.py", release_name], env=working_env)
        print(' == result create installer:', result.returncode, flush=True)
        os.chdir(current_directory)
    elif platform.system() == "Darwin":
        # TODO: Correct path...
        # os.chdir(f"{NEON_REPO}/res/macos")
        os.chdir(f"res/macos")
        result = subprocess.run(["/bin/bash", "create_installer.sh", release_name], env=working_env)
        print(' == result create installer:', result.returncode, flush=True)
        os.chdir(current_directory)

    if result.returncode:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
