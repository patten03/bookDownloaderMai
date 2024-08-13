from PIL import Image
import os
import shutil

def makePdfBook(folder: str):
    # make images list
    print(f"Загрузка всех изображение из папки \"{folder}\" в pdf")
    images = []
    for file in os.listdir("./" + folder):
        if file.endswith(".png"):
            images.append(Image.open("./" + folder + "/" + file))

    # save pdf
    print(f"Сохрание книги под названием \"{folder}.pdf\"")
    images[0].save(
        folder + ".pdf",
        "PDF",
        resolution = 100.0,
        save_all = True,
        append_images = images[1:]
    )

    # delete all unnecessary folder with raw images
    print(f"Удаление папки \"{folder}\"")
    shutil.rmtree(folder)
