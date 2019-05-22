from ProcessCSV import ProcessCSV

p = ProcessCSV()
p.loadFile('train.csv')
p.loadTags('Structure.txt')
p.constructRows()
p.constructColumns()
p.constructFillers()
p.findRowWithEmptyClassAndDelete()

print(p.getRows())

# print(FindingCommonValue(p.getColumns()['job']))
# print(NumericAverage(p.getColumns()['previous']))
