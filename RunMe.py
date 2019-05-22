from ProcessCSV import ProcessCSV

p = ProcessCSV()
p.loadFile('train.csv')
p.loadTags('Structure.txt')

p.constructColumns()
print('Columns are: \n', p.getColumns())
p.constructFillers()
print('removing lines with empty class')
p.findRowWithEmptyClassAndDelete()

# print(p.getFillers())
print('After removing lines columns are: \n', p.getColumns())
# p.findEmptyColumn()
# print(p.getColumns())


# print(FindingCommonValue(p.getColumns()['job']))
# print(NumericAverage(p.getColumns()['previous']))
