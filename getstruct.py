import os

def list_files(startpath):
    with open('tree.txt', 'w') as f:
        for root, dirs, files in os.walk(startpath):
            level = root.replace(startpath, '').count(os.sep)
            indent = ' ' * 4 * (level)
            f.write('{}{}/\n'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for filename in files:
                f.write('{}{}\n'.format(subindent, filename))

list_files('.')
