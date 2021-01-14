'''
A dumper for DDLC's 'images.rpa'

Usage:
1. Put 'images.rpa' here
2. Run this script
Images will be placed in 'output/'
'''

import os

PNG_BEGIN = bytes.fromhex('8950 4E47 0D0A 1A0A')
PNG_END = bytes.fromhex('0000 0000 4945 4E44 AE42 6082')

with open('images.rpa', 'rb') as f:
    file_images = f.read()

os.makedirs('output', exist_ok=True)

idx = 0
while True:
    try:
        begin = file_images.index(PNG_BEGIN)
    except ValueError:
        break
    end = file_images.index(PNG_END)

    fname = f'output/{idx}.png'
    with open(fname, 'wb') as f:
        f.write(file_images[begin:end])
        f.write(PNG_END)
    print(fname)

    idx += 1
    file_images = file_images[end+len(PNG_END):]