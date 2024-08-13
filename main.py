import httpInteraction as hi
import pdfMaker as pm
   
def main():
    # download pages
    folder = hi.downloadBook()
    
    # make bind pages as pdf file
    pm.makePdfBook(folder)
    
    # prevent closing program
    print("Скачивание завершено, для закрытия программы нажмите Enter...")
    input()

if __name__ == "__main__":
    main()