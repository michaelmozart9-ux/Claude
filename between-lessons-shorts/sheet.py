import sys, glob
from PIL import Image
d=sys.argv[1]; fs=sorted(glob.glob(f'{d}/test-*.jpg'),key=lambda f:float(f.split('test-')[1][:-4]))
W=270;H=480;n=len(fs);cols=min(6,n);rows=(n+cols-1)//cols;im=Image.new('RGB',(W*cols,H*rows))
for i,f in enumerate(fs): im.paste(Image.open(f).resize((W,H)),((i%cols)*W,(i//cols)*H))
im.save(f'{d}/sheet.jpg')
