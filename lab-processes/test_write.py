import os
with open('myfile','wb') as f:
  while True:
    f.write(os.urandom(1024))