import file_processing
import logging
import shutil
import os

path_cwd = os.path.dirname(os.path.realpath(__file__))
down = path_cwd + '/download'

def split(file,dir):
    if os.path.exists(path_cwd + f"\\out\\{file}\\"):
        folder = os.listdir(path_cwd + f"\\out\\{file}\\")
        for i in range(len(folder)):
            folder[i] = path_cwd + f"\\out\\{file}\\" + folder[i]
        for i in range(len(folder)):
            if os.path.exists(folder[i]):
                os.remove(folder[i])
    else:
        os.mkdir(path_cwd + f"\\out\\{file}\\")

    shutil.copyfile(dir,
                    path_cwd + f"\\out\\{file}\\" + file)

    fsplitter = file_processing.FileProcessor()

    #Set size of each chunk, for example: 25 mb
    p_size = 20

    #File to split and subdir where to save chunks
    from_file = path_cwd + f"\\out\\{file}\\" + file
    to_dir = path_cwd + f"\\out\\{file}\\"

    if not os.path.exists(to_dir):
        try:
            os.mkdir(to_dir)
        except PermissionError as perm_err:
            logging.error(str(perm_err))
        except OSError as os_err:
            logging.error(str(os_err))

    absfrom, absto = map(os.path.abspath, [from_file, to_dir])
    print('Splitting', absfrom, 'to', absto, 'by', p_size, 'mb...')

    #Split now
    fsplitter.split_file_by_size(from_file, p_size, to_dir)

    if os.path.exists(path_cwd + f"\\out\\{file}\\" + file):
        os.remove(path_cwd + f"\\out\\{file}\\" + file)

def join(file):
    fjoiner = file_processing.FileProcessor()

    #Set the size-value for reading chunks, for example: 25 mb
    readsize = 20

    #Set chunks dir and dest filename
    from_dir = path_cwd + f"\\out\\{file}\\"
    to_file = down + "\\" + file

    absfrom, absto = map(os.path.abspath, [from_dir, to_file])
    print('Joining', absfrom, 'to', absto, 'by', readsize)
    #Join now
    fjoiner.join_file(from_dir, readsize, to_file)