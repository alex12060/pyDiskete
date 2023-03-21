class Disk:

    FileSystem = {
        'Blocks': [],
        'UsedBlocks': [],
        'DeletedBlocks': []
    }

    DiskProperties = {
        'DiskSize': 368640,
        'FreeSize': 368640,
        'BlockSize': {
            'min': 18,
            'max': 32768
        },
        'ReadOnly': False,
        'FileSystemAlias': ['ID', 'name', 'size', 'date'],
    }

    def write(self, idx, block):
        if (self.isFileSystemReadOnly()):
            raise SystemError("File system is read only!")

        self.decreaseFreeSize(block.getBlockSize())
        self.FileSystem['Blocks'].insert(idx, block)
        self.FileSystem['UsedBlocks'].insert(idx, idx)

    def update(self, idx, block):
        if (self.isFileSystemReadOnly()):
            raise SystemError("File system is read only!")

        self.FileSystem['Blocks'][idx] = block

    def remove(self, idx):
        if (self.isFileSystemReadOnly()):
            raise SystemError("File system is read only!")

        self.increaseFreeSize(self.get(idx).getBlockSize())
        self.FileSystem['DeletedBlocks'].insert(idx, idx)
        self.FileSystem['UsedBlocks'].remove(idx)

    def get(self, idx):
        return self.FileSystem['Blocks'][idx]

    def delete(self, block, idx):
        match block:
            case 'used':
                self.FileSystem['UsedBlocks'].remove(idx)
            case 'deleted':
                self.FileSystem['DeletedBlocks'].remove(idx)

    def add(self, block, idx):
        match block:
            case 'used':
                self.FileSystem['UsedBlocks'].insert(idx, idx)
            case 'deleted':
                self.FileSystem['DeletedBlocks'].insert(idx, idx)

    def getDiskSize(self):
        return self.DiskProperties.get('DiskSize')

    def getFreeSpace(self):
        return self.DiskProperties.get('FreeSize')

    def increaseFreeSize(self, inputSize):
        self.DiskProperties['FreeSize'] = self.DiskProperties.get('FreeSize') + inputSize

    def decreaseFreeSize(self, inputSize):
        if (self.DiskProperties.get('FreeSize') - inputSize < 0):
            raise ValueError("Not enough free space on disk!")

        self.DiskProperties['FreeSize'] = self.DiskProperties.get('FreeSize') - inputSize

    def getFileSystem(self):
        return self.FileSystem

    def getDiskProperties(self):
        return self.DiskProperties

    def setFileSystem(self, FileSystem):
        self.FileSystem = FileSystem

    def isFileSystemReadOnly(self):
        return self.DiskProperties.get('ReadOnly')

    def setFileSystemReadOnly(self):
        self.DiskProperties['ReadOnly'] = True

    def unsetFileSystemReadOnly(self):
        self.DiskProperties['ReadOnly'] = False

    def getLastUsedIdx(self):
        try:
            return self.FileSystem['UsedBlocks'][-1]
        except:
            return -1

    def getLastDeletedIdx(self):
        try:
            return self.FileSystem['DeletedBlocks'][-1]
        except:
            return -1