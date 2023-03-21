from IO import IO
from FileSystem import Disk
from DiskBlock import DiskBlock

# Инициируем диск
FS = Disk()

# Инициируем обработчик и передаем диск
DiskIO = IO(FS)

#DiskIO.list()
DiskIO.delete(1)
#DiskIO.create(DiskBlock('test1', 3276).make())
#DiskIO.create(DiskBlock('test3', 544).make())
#DiskIO.delete(1)
#DiskIO.create(DiskBlock('test4', 544).make())
#DiskIO.read(4)

#DiskIO.create(DiskBlock('test5', 544).make())
#DiskIO.delete(1)
DiskIO.list()