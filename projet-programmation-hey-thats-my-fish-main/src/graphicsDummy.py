class GraphicsDummy():
    display = True
    def __init__(self):
        pass

    def showWorld(self, world):
        pass

    def endDisplay(self):
        self.display = False

    def quit(self):
        self.endDisplay()
        exit()