from zipfile import ZipFile
import os

for f in os.listdir('code'):
    file = f.split('.')
    if file[1] == 'py':
        zf = ZipFile(os.path.join('zips', file[0], '.zip'), mode='w')
        zf.write(os.path.join('code',f))
        zf.close()