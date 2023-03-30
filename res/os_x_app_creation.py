#! /usr/bin/env python
import os
import shutil
import subprocess

MAIN_WINDOW_UI_FILE = 'src/cmlibs/neon/ui/ui_mainwindow.py'


def remove_parent_of_menubar():
    with open(MAIN_WINDOW_UI_FILE, 'r+') as f:
        s = f.read()
        f.seek(0)
        c = s.replace('self.menubar = QtGui.QMenuBar(MainWindow)', 'self.menubar = QtGui.QMenuBar(None)')
        f.write(c)
        f.truncate()


def create_softlink_to_zinc(directory):
    subprocess.call(['ln', '-s', directory, 'zinc'])


def execute_py2app_build():
    subprocess.call(['python', 'setup.py2app.py', 'py2app'])


def rename_app():
    shutil.move('neon.app', 'Neon.app')
    shutil.move('Neon.app/Contents/MacOS/neon', 'Neon.app/Contents/MacOS/Neon')
    with open('Neon.app/Contents/Info.plist', 'r+') as f:
        s = f.read()
        f.seek(0)
        c = s.replace('neon', 'Neon')
        f.write(c)
        f.truncate()


def mv_app(destination):
    target_location = os.path.join(destination, 'Neon.app')
    if os.path.exists(target_location):
        shutil.rmtree(target_location)
    shutil.move('Neon.app', target_location)


def rm_build_dist():
    shutil.rmtree('build')
    shutil.rmtree('dist')


def rm_softlink():
    os.remove('zinc')


def undo_code_change():
    subprocess.call(['git', 'co', '--', MAIN_WINDOW_UI_FILE])


def main():
    import cmlibs.zinc.context

    directory = os.path.dirname(cmlibs.zinc.context.__file__)
    base_dir = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
    destination = os.environ['HOME']
    pwd = os.getcwd()
    os.chdir(base_dir)
    remove_parent_of_menubar()
    os.chdir(os.path.join(base_dir, 'src', 'cmlibs'))
    create_softlink_to_zinc(directory)
    os.chdir(os.path.join(base_dir, 'src'))
    execute_py2app_build()
    os.chdir(os.path.join(base_dir, 'src', 'dist'))
    rename_app()
    mv_app(destination)
    os.chdir(os.path.join(base_dir, 'src'))
    rm_build_dist()
    os.chdir(os.path.join(base_dir, 'src', 'cmlibs'))
    rm_softlink()
    os.chdir(base_dir)
    undo_code_change()
    os.chdir(pwd)
    print('Created new Neon application at: ', os.path.join(destination, 'Neon.app'))

if __name__ == '__main__':
    main()

