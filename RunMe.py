from ProcessCSV import ProcessCSV

p = ProcessCSV()
p.loadFile('train.csv')
p.loadTags('Structure.txt')


p.constructColumns()

p.constructFillers()

p.findRowWithEmptyClassAndDelete()

p.findEmptyColumn()

p.findClassEntropy()
p.findSplitPosition(p.getColumns()['age'])
# print(p.getClassesCounter())
# print(p.getTotalClasses())
# print(p.getClassesEntropy())
