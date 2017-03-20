import os,re,sys
from optparse import OptionParser
from distutils.sysconfig import get_python_lib

base_dir = sys.path[0]

SEP = os.path.sep

lib_dir = get_python_lib()
pth = lib_dir + SEP + 'data_mover.pth'
lib_dir_for_data_mover = base_dir

print(lib_dir_for_data_mover)

# Install python pth file
if not os.path.exists(pth):
    print("Start to install " + pth)
    try:
        fh = open(pth,'w')
        fh.write(lib_dir_for_data_mover + '\n')
        print(">>" + lib_dir_for_data_mover)
        print(pth + " has been installed successfully.")
    except:
        print('Can\'t open ' + pth)
    finally:
        fh.close()
else:
    print(pth + " is already exists.")
