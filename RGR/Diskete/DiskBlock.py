class DiskBlock:

    _BlockID = -1
    _BlockName = ""
    _BlockSize = 0
    _BlockCreateDate = ""

    def __init__(self, BlockName, BlockSize):
        self.setBlockName(BlockName)
        self.setBlockSize(BlockSize)
        self.setBlockDate()

    def make(self):
        return self

    def setBlockID(self, id):
        self._BlockID = int(id)

    def setBlockSize(self, size):
        self._BlockSize = int(size)

    def setBlockName(self, blockName):
        self._BlockName = blockName

    def setBlockDate(self):
        from datetime import date

        dt = date.today()
        self._BlockCreateDate = dt.strftime("%d.%m.%Y %H:%M:%S")

    def getBlockID(self):
        return self._BlockID

    def getBlockSize(self):
        return self._BlockSize

    def getBlockName(self):
        return self._BlockName

    def getBlockDate(self):
        return self._BlockCreateDate

    def __str__(self):
        return "[" + str(self._BlockID) + " / " + str(self._BlockName) + " / " + str(self._BlockSize) + " / " + str(self._BlockCreateDate) + "]"

