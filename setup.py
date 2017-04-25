from shared.path import getScriptDirectory

import shutil
import sys
import os
import os.path
import platform
from cx_Freeze import setup,Executable
from distutils.sysconfig import get_python_lib

def list_all_files(path):
  entrylist = os.listdir(path)
  flist = []
  for entry in entrylist:
    fentry = os.path.join(path, entry)
    if os.path.isdir(fentry):
      nflist = list_all_files(fentry)
      flist = flist + nflist
    else:
      flist.append(fentry)
  return flist

# required to initialize zope packages
# that means that the zope package (if installed)
# needs to contain an __init__.py, which it doesn't from the start
def initialize_zope_package():
  lib_dir = get_python_lib()
  if not os.path.exists(os.path.join(lib_dir, 'zope')):
    print "Zope package not found. This setup file won't work without at least zope.interface installed"
    sys.exit()
  if not os.path.exists(os.path.join(lib_dir, 'zope', '__init__.py')):
    print "No __init__.py file found for zope package, creating it manually"
    open(os.path.join(lib_dir, 'zope', '__init__.py'), 'w').write('')

include_files = []

# will later be needed for the client
#include_files+=[(os.path.join(script.Path, "accessible_output", "lib", x), os.path.join("lib", x)) for x in os.listdir(os.path.join(script.Path, #"accessible_output", "lib"))]

build_exe_options = {
                     "includes": [
                                  "zope.interface"
                                 ],
                     "excludes": [
                                  "bz2",
                                  "tar",
                                  "Tkinter"
                                 ],
                     "include_files": include_files
                    }

# preparing setup package environment
initialize_zope_package()

setup(
  name = "cards-against-humanity",
  version = "0.1",
  description = "Cards Against Humanity Online Game",
  options = {
    'build_exe' : build_exe_options
  },
  executables = [
    Executable(
      'editor.py',
      base=(None if platform.system() != 'Windows' else 'Win32GUI')
    ),
    Executable(
      'server.py',
      base=None
    )
  ]
)
"""
build_dir = os.path.join(script.Path, 'build', os.listdir(os.path.join(script.Path, 'build'))[0])

if platform.system()=='Windows':
  import zipfile
  zip=zipfile.ZipFile(os.path.join(script.Path, '%s-%s.zip'%(script.Name, script.Version)), "w")
  for file in list_all_files(build_dir):
    zip.write(file,'%s-%s\\%s'%(script.Name, script.Version, os.path.relpath(file,build_dir)), zipfile.ZIP_DEFLATED)
  zip.close()
else:
  import tarfile
  tar=tarfile.open('%s-%s.tar.gz'%(script.Name, script.Version),'w:gz')
  tar.add(build_dir, '%s-%s'%(script.Name, script.Version))
  tar.close()
shutil.rmtree(os.path.join(script.Path, "build"))
"""