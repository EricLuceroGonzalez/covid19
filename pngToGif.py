from PIL import Image
import glob
import pathlib
thePath = str(pathlib.Path(__file__).parent.absolute()) + '/plots/'
print(thePath)

# print(glob.glob(thePath+'/*.png'))
# image_files = [thePath + '/' + f for f in glob.glob('*.png')]
# print(image_files)
# for filepath in image_files:
#     callimage = Image.open(filepath).load()

# Create the frames
frames = []
imgs = glob.glob(thePath+"/days*")
print(glob.glob('*.png'))
print(imgs)
for i in imgs:
    new_frame = Image.open(i)
    frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save('png_to_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=600, loop=0)
