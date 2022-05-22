from zipfile import ZipFile
import os

print(os.listdir)
for f in os.listdir('code'):
    file = f.split('.')
    if file[1] == 'py':
        zf = ZipFile(f'zips\\{file[0]}.zip', mode='w')
        zf.write(f'code\\{f}')
        zf.close()