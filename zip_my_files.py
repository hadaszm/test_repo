from zipfile import ZipFile
import os

os.makedirs('zips', exist_ok=True)
for f in os.listdir('code'):
    file = f.split('.')
    if file[1] == 'py':
        try:
            zf = ZipFile(os.path.join('zips', f'{file[0]}.zip'), mode='w')
            zf.write(os.path.join('code', f))
            zf.close()
        except Exception as e:
            print(e)
