from ProcessCSV import ProcessCSV

p = ProcessCSV()
p.open_files('d:/Dev/Python/Data Mining Project')
p.clean_up()
# print(p.entropy_discretization(p.columns['balance'], 3))
p.discretisize(3)
print(p.columns)


# print(p.columns['age'])
# print(p.build_bins(3))
