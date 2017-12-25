# #### this code only should have required ODB txt files from previous Code in current directory
import glob, os,PyQt5
import matplotlib.pyplot as pyplot
plot_names =[]
row=[]
disp=[]
load=[]
exp_load=[]
exp_disp=[]
for file in glob.glob("*.txt"):
    plot_names.append(file)

no_files=len(plot_names)

for xx in range(0,no_files):
     with open(plot_names[xx], 'r') as f:
        lines = f.readlines()
        for data in lines:
            row = data.split(';')
            load.append(float(row[0])*1.4)
            disp.append(float(row[1])*1.4)
        print load,disp
        pyplot.plot(disp,load,label=xx)#plot_names[xx])#, label=plot_names[xx])
        load = []
        disp = []

nameOFexp_filee='al2mm_45EXP.csv'
with open(nameOFexp_filee, 'r') as file:
    lines = file.readlines()
    for data in lines:
        row = data.split('	')
        exp_load.append(float(row[0]))
        exp_disp.append(float(row[1]))
    pyplot.plot(exp_disp,exp_load, label=nameOFexp_filee)
pyplot.xlabel('Displacement')
pyplot.ylabel('Load')
pyplot.legend()
pyplot.title('AL 2mm 45degrees')
pyplot.show()

