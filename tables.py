import pandas as pd
import numpy as np
stroopdata = pd.read_csv('stroopdata.csv')

table = stroopdata.describe().to_latex()
data_describe = 'data_describe.tex'
f = open(data_describe, 'w')
f.write( table )
f.close()

data = stroopdata.max() - stroopdata.min()
file = "range.txt"
f = open(file, 'w')
f.write( str(data) )
f.close()
