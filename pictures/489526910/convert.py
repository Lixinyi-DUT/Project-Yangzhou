from wand.image import Image

diag='diagram.pdf'

with(Image(filename=diag,resolution=200)) as source:
    images=source.sequence
    pages=len(images)
    for i in range(pages):
        Image(images[i]).save(filename=str(i+1)+'.png')
