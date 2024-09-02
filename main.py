from megaverse import Megaverse, Shape

def main():
    mv = Megaverse()
    
    #Call to create cross image
    mv.createPolyanetsCross()

    #Deleting any shape at any (row, column)
    mv.deleteShape(3, 4, Shape.SOLOONS)

    #Call to create a big megaverse
    mv.createCrossmintLogo()
    
if __name__ == "__main__":
    main()