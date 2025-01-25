# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 6 Assignment
#
# Usage: python3 Magpantay_Kimberly_Assignment_Week6.py -g Arntl,Clock,Dbp,Per1,Per2,Per3,Nr1d1,Insig2,Cry1 -p BME163_Input_Data_Assignment6.phase -e BME163_Input_Data_Assignment6.exp -o Magpantay_Kimberly_Assignment_Week6.png
# '''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import matplotlib.patheffects as pe
import numpy as np
import matplotlib.image as mpimg
import argparse
import matplotlib

plt.style.use('BME163') # For stylesheet

# Parse arguments for input and output files
parser = argparse.ArgumentParser() # A way to get info from your command line
parser.add_argument('--outFile','-o' ,type=str,action='store',default='output.png',help='output file')
parser.add_argument('--phaseFile','-p' ,type=str,action='store',default='BME163_Input_Data_Assignment6.phase', help='phase file')
parser.add_argument('--expFile','-e' ,type=str,action='store',default='BME163_Input_Data_Assignment6.exp', help='exp file')  
parser.add_argument('--genes','-g', type=str, action='store', default='', help='genes')

args = parser.parse_args()
outFile=args.outFile
phaseFile=open(args.phaseFile)
expFile=open(args.expFile)
geneLabels = args.genes.split(',') if args.genes else []

'''Figure Initialization'''
fig_1 = plt.figure(figsize=(5,3))
panel1 = plt.axes([0.7/5 , 0.3/3 , 0.75/5 , 2.5/3],frameon=True)
plt.xlabel('CT')
panel2 = plt.axes([1.5/5 , 1.45/3 , 0.1/5 , 0.2/3],frameon=True)

# Adjust params for panels
panel1.tick_params(bottom=True, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
panel2.tick_params(bottom=False, labelbottom=False, \
                   left=False, labelleft=False, \
                   right=True, labelright=True, \
                   top=False, labeltop=False)
panel1.set_xlim([0,12])
panel2.set_ylim(0, 101)
panel2.set_yticklabels(['Min','Max']) # Overwrite y_lim 


'''Viridis Colormap for Panel 2'''
viridis5 = (253/255, 231/255, 37/255)
viridis4 = (94/255, 201/255, 98/255)
viridis3 = (33/255, 145/255, 140/255)
viridis2 = (59/255, 82/255, 139/255)
viridis1 = (68/255, 1/255, 84/255)

R1=np.linspace(viridis1[0],viridis2[0],26)
G1=np.linspace(viridis1[1],viridis2[1],26)
B1=np.linspace(viridis1[2],viridis2[2],26)

R2=np.linspace(viridis2[0],viridis3[0],26)
G2=np.linspace(viridis2[1],viridis3[1],26)
B2=np.linspace(viridis2[2],viridis3[2],26)

R3=np.linspace(viridis3[0],viridis4[0],26)
G3=np.linspace(viridis3[1],viridis4[1],26)
B3=np.linspace(viridis3[2],viridis4[2],26)

R4=np.linspace(viridis4[0],viridis5[0],26)
G4=np.linspace(viridis4[1],viridis5[1],26)
B4=np.linspace(viridis4[2],viridis5[2],26)

R=np.concatenate((R1[:-1],R2[:-1],R3[:-1],R4),axis=None)
G=np.concatenate((G1[:-1],G2[:-1],G3[:-1],G4),axis=None)
B=np.concatenate((B1[:-1],B2[:-1],B3[:-1],B4),axis=None)

viridis=[]
for index in range(0,101,1):
    viridis.append((R[index],G[index],B[index]))
    
for index in range(0,101,1):
    rectangle=mplpatches.Rectangle((0, index), 101, 1, # Bottom Half
                                facecolor=(viridis[index]),
                                edgecolor='black',
                                linewidth=0) 
    panel2.add_patch(rectangle)


'''Initializate Dictionaries'''
# Obtain PHASE DATA and put it in dictionary
phaseDict = {} # identifier : peak_phase
next(phaseFile) # Skips first line
for line in phaseFile: 
	l = line.strip().split()
	identifier = l[0] # Read identifier in 1st column
	phase = float(l[1]) # Read phase in 2nd column
	phaseDict[identifier] = phase
phaseFile.close()

# Obtain EXP DATA and put it in dictionary
expDict = {} # Identifier : [Array]
gene_positions = {}
geneToIdentifier = {}
next(expFile)
for line in expFile:
	l = line.strip().split()
	identifier = l[1]
	values = [float(l[i]) for i in range(4,12)]
	expDict[identifier] = values
    
	if l[0] in geneLabels:
          geneToIdentifier[l[0]] = identifier
          
expFile.close()

print(gene_positions)
print(geneToIdentifier)

'''HeatMap'''
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

dataList = []
for identifier, values in expDict.items():
    values = moving_average(values, 1) # Moving average with window size 1
    values = (values - min(values)) / (max(values) - min(values)) * 100 # Normalize
    dataList.append((values.astype(int), identifier, phaseDict[identifier]))
    
# expDict : Identifier : [Array], 
# Gene Positions - Gene: y
# GeneToIdentifier - Gene : Identifier
# dataList: [Array], Phase
# phaseDict: Identifier: Phase
print(dataList)
y=0
for data, identifier, phase in sorted(dataList, key=lambda x:x[-1], reverse=True): # Sorted based on peak phase
    for pos in range(len(data)):
        x=data[pos]
        rectangle = mplpatches.Rectangle([pos,y],1,1,
                                 facecolor=viridis[x],
                                 edgecolor='black',
                                 linewidth=0
                                 )
        panel1.add_patch(rectangle)
        for gene, geneIdentifier in geneToIdentifier.items():
              if geneIdentifier == identifier:
                   gene_positions[gene] = y
    y+=1
    
print(gene_positions)

panel1.set_xlim(0,8)
panel1.set_xticks([i+0.5 for i in range(8)])
panel1.set_xticklabels(['0','','6','','12','','18', ''])
panel1.set_ylim(0,y+1)

# Set the y-ticks and labels
if gene_positions:
    y_ticks = list(gene_positions.values()) # Number to plot at
    y_ticklabels = list(gene_positions.keys()) # Gene Name
    
    # Adjust y-tick positions based on where the array is placed on the y-axis
    y_tick_positions = [tick_pos + 0.5 for tick_pos in y_ticks]
    
    panel1.set_yticks(y_tick_positions)
    panel1.set_yticklabels(y_ticklabels)

plt.savefig(outFile, dpi=600)