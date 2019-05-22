from ProcessCSV import ProcessCSV

p = ProcessCSV()
p.loadFile('train.csv')
p.loadTags('Structure.txt')


p.constructColumns()
print('Columns are: \n', p.getColumns())
p.constructFillers()
print(p.getFillers())
print('removing lines with empty class')
p.findRowWithEmptyClassAndDelete()

print('After removing lines columns are: \n', p.getColumns())
p.findEmptyColumn()
print('Filling blanks: \n', p.getColumns())
