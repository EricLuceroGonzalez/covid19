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
imgs = glob.glob(thePath+"/daysWithVirus-*")
print(glob.glob('*.png'))
print(len(imgs))
for i in range(10, 31):
    for j in imgs:
        if j == thePath+"daysWithVirus-"+str(i)+'-3.png':
            new_frame = Image.open(j)
            frames.append(new_frame)

# Save into a GIF file that loops forever
frames[0].save(thePath+'covid_gif.gif', format='GIF',
               append_images=frames[1:],
               save_all=True,
               duration=400, loop=2)