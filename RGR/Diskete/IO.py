class IO:

    _FileSystem = None

    CRED = '\033[91m' # ascii подсветка красным
    CEND = '\033[0m'  # ascii подсветка красным

    def __init__(self, FileSystem):
        self._FileSystem = FileSystem

    def list(self):
        self.makeList()
        print(self._FileSystem.getFileSystem())

    def makeList(self):
        DB = self._FileSystem.FileSystem.get('DeletedBlocks')
        print(self._FileSystem.DiskProperties.get('FileSystemAlias'))
        for Block in self._FileSystem.getFileSystem().get('Blocks'):
            if (DB.count(Block.getBlockID()) > 0):
                print(self.CRED + str(Block) + self.CEND)
            else:
                print(str(Block))
        print("Total space: " + str(self._FileSystem.getDiskSize()))
        print("Free space: " + str(self._FileSystem.getFreeSpace()))

    def hasNameInFS(self, BlockName):
        FS = self._FileSystem.getFileSystem()

        if (len(FS['UsedBlocks']) == 0):
            return False

        for BlockID in FS['UsedBlocks']:
            if (self.getByID(BlockID).getBlockName() == BlockName):
                return True

        return False

    def getByID(self, id):
        try:
            return self._FileSystem.getFileSystem().get('Blocks')[id]
        except:
            return None

    def create(self, Block):
        fullBlockUpdated = False

        FileProps = self._FileSystem.getDiskProperties()['BlockSize']

        if (Block.getBlockSize() < FileProps.get('min') or Block.getBlockSize() > FileProps.get('max')):
            raise ValueError('Block size must be between ' + str(FileProps.get('min')) + ' and ' + str(FileProps.get('max')))

        if (self.hasNameInFS(Block.getBlockName())):
            raise ValueError('Block ' + Block.getBlockName() + ' already exists!')

        freeBlockID = self.checkInUsedBlocks(Block)
        idx = self.getLastIdx() + 1

        if (type(freeBlockID) is int):
            fullBlockUpdated = self.processUpdateFreeSizeBlock(freeBlockID, Block)

        if (fullBlockUpdated == False):
            Block.setBlockID(idx)
            self._FileSystem.write(idx, Block)

    def processUpdateFreeSizeBlock(self, idx, Block):
        # 1. Изменить размер удаленного блока

        oldBlock = self.read(idx)

        # 1.1 Получаем разность размеров блоков

        blockSizeDiff = oldBlock.getBlockSize() - Block.getBlockSize()

        # 1.2 Если разность равна 0, то убираем информацию о блоке, что он удален и тупо заполняем информацию на старом блоке

        if (blockSizeDiff == 0):
            Block.setBlockID(idx)
            self._FileSystem.update(idx, Block)
            self._FileSystem.delete('deleted', idx)
            self._FileSystem.add('used', idx)

            return True
        else:
            oldBlock.setBlockSize(blockSizeDiff)
            self.update(idx, oldBlock)

            return False


    def checkInUsedBlocks(self, Block):
        DeletedBlocks = self._FileSystem.getFileSystem().get('DeletedBlocks')

        for BlockIdx in DeletedBlocks:
            if (self.getByID(BlockIdx).getBlockSize() >= Block.getBlockSize()):
                return BlockIdx

        return False

    def isBlockDeleted(self, BlockID):
        DeletedBlocks = self._FileSystem.getFileSystem().get('DeletedBlocks')

        if DeletedBlocks.count(BlockID) > 0:
            return True

        return False

    def isBlockUsed(self, BlockID):
        UsedBlocks = self._FileSystem.getFileSystem().get('UsedBlocks')

        if UsedBlocks.count(BlockID) > 0:
            return True

        return False

    def getDeletedBlocks(self):
        Blocks = []
        DeletedBlocks = self._FileSystem.getFileSystem().get('DeletedBlocks')

        for BlockIdx in DeletedBlocks:
            Blocks.append(self.getByID(BlockIdx))

        return Blocks

    def getUsedBlocks(self):
        Blocks = []
        UsedBlocks = self._FileSystem.getFileSystem().get('UsedBlocks')

        for BlockIdx in UsedBlocks:
            Blocks.append(self.getByID(BlockIdx))

        return Blocks

    def delete(self, idx):
        if (self.isBlockUsed(idx) == True):
            self._FileSystem.remove(idx)

    def update(self, idx, data):
        self._FileSystem.update(idx, data)

    def read(self, idx):
        try:
            return self._FileSystem.getFileSystem()['Blocks'][idx]
        except:
            raise ValueError("Cannot read block with id " + str(idx))

    def getIdxByBlockName(self, BlockName):
        FS = self._FileSystem.getFileSystem()['UsedBlocks']

        for BlockIdx in FS:
            if self.read(BlockIdx).getBlockName() == BlockName:
                return BlockIdx

        return None

    def getLastIdx(self):
        deletedIdxs = self._FileSystem.getLastDeletedIdx()
        usedIdxs = self._FileSystem.getLastUsedIdx()

        if (deletedIdxs > usedIdxs):
            return deletedIdxs
        else:
            return usedIdxs