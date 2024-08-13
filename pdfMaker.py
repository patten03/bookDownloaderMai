from PIL import Image
import os

def makePdfBook(folder: str):
    # make images list
    images = []
    for file in os.listdir("./" + folder):
        if file.endswith(".png"):
            images.append(Image.open("./" + folder + "/" + file))
            
    # save pdf
    images[0].save(
        folder + ".pdf",
        "PDF",
        resolution = 100.0,
        save_all = True,
        append_images = images[1:]
    )