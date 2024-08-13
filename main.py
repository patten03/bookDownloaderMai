import httpInteraction as hi
import pdfMaker as pm
   
def main():
    # download pages
    folder = hi.downloadBook()
    
    # make bind pages as pdf file
    pm.makePdfBook(folder)

if __name__ == "__main__":
    main()