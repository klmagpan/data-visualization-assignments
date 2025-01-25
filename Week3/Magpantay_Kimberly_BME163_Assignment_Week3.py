# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 3 Assignment
#
# Usage: python3 Magpantay_Kimberly_BME163_Assignment_Week3.py -p BME163_Input_Data_Week3.position.tsv -c BME163_Input_Data_Week3.celltype.tsv -o Magpantay_Kimberly_BME163_Assignment_Week3.png
# '''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import matplotlib.patheffects as pe
import numpy as np
import argparse
import matplotlib

plt.style.use('BME163') # For stylesheet

# Parse arguments for input and output files
parser = argparse.ArgumentParser() # A way to get info from your command line
parser.add_argument('--outFile','-o' ,type=str,action='store',default='output.png',help='output file')
parser.add_argument('--positionFile','-p' ,type=str,action='store',default='position.tsv', help='position file') # Making use of default to rename output file name
parser.add_argument('--celltypeFile','-c' ,type=str,action='store', default='celltype.tsv',help='celltype file')
args = parser.parse_args()
outFile=args.outFile
posFile=open(args.positionFile)
cellFile=open(args.celltypeFile)

# Intialize figure sizes
figureWidth=5
figureHeight=3

panelWidth=1.5
panelHeight=1.5

relativePanelWidth=panelWidth/figureWidth
relativePanelHeight=panelHeight/figureHeight

# Create figure
plt.figure(figsize=(figureWidth,figureHeight))

# Create panels: [left, bottom, width, height] and add axis labels
panel1=plt.axes([0.5/figureWidth,0.5/figureHeight,relativePanelWidth,relativePanelHeight])
plt.xlabel('tSNE 2')
plt.ylabel('tSNE 1')
panel2=plt.axes([2.5/figureWidth,0.5/figureHeight,relativePanelWidth,relativePanelHeight])
plt.xlabel('tSNE 2')
plt.ylabel('tSNE 1')
panel3=plt.axes([4.0/figureWidth,1.1/figureHeight,0.1/figureWidth,0.3/figureHeight])

# Adjust params for panels
panel1.tick_params(bottom=True, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
panel2.tick_params(bottom=True, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
panel3.tick_params(bottom=False, labelbottom=False, \
                   left=False, labelleft=False, \
                   right=True, labelright=True, \
                   top=False, labeltop=False)

# Limits
panel1.set_xlim(-30,30)
panel1.set_ylim(-40,30)
panel2.set_xlim(-30,30)
panel2.set_ylim(-40,30)
panel3.set_ylim(0, 101) 

# Obtain celltype data and put it in dictionary
celltypeDict = {} # strand : type
for line in cellFile: 
  # print(line)
  if line[0] != '#':
    l = line.strip().split()
    barcode = l[2]
    ct = l[1]
    celltypeDict[barcode] = ct
cellFile.close()

# Obtain positions from position file
posDict = {} # strand : position
for line in posFile:
  l = line.strip().split()

  x = float(l[1])
  y = float(l[2])

  barcode = l[0]
  posDict[barcode] = [x,y]
posFile.close()

# COlor
iBlue=(88/255,85/255,120/255)
iGreen=(120/255,172/255,145/255)

# Colormap Code
viridis = [
	(253/255, 231/255, 37/255),
	(94/255, 201/255, 98/255),
	(33/255, 145/255, 140/255),
	(59/255, 82/255, 139/255),
	(68/255, 1/255, 84/255)  
]

RBottom = []
GBottom = []
BBottom = []
colormap = []

for i in range(len(viridis) - 1, 0, -1): # Reverse Order
    color1 = viridis[i]
    color2 = viridis[i - 1]

    R = np.linspace(color1[0], color2[0], 27)
    G = np.linspace(color1[1], color2[1], 27)
    B = np.linspace(color1[2], color2[2], 27)
    RBottom = np.concatenate((RBottom[:-1], R), axis=None)
    GBottom = np.concatenate((GBottom[:-1], G), axis=None)
    BBottom = np.concatenate((BBottom[:-1], B), axis=None)

for index in range(0,101,1):
    colormap.append((RBottom[index],GBottom[index],BBottom[index]))

#                                 (left,bottom),width,height
for index in range(0,101,1):
    rectangle=mplpatches.Rectangle((0, index), 101, 1, # Bottom Half
                                facecolor=(colormap[index]),
                                edgecolor='black',
                                linewidth=0) 
    panel3.add_patch(rectangle)

points = [] # Initialize for panel2

# Plot points for panel1
for key,value in posDict.items():
   
   x = value[0]
   y = value[1]

   points.append((x,y))

   cellType = celltypeDict.get(key)
   if cellType == 'tCell':
      color = iGreen
   if cellType == 'monocyte':
      color = 'grey'
   if cellType == 'bCell':
      color = iBlue
   panel1.plot(x, y,
				marker='o',
				markersize=4,
				markeredgewidth=0.1,
				markeredgecolor='black',
				markerfacecolor=color,
				linewidth=0,
				linestyle='-')

# Panel 2 Density calculation
minimum_distance = 4.915
for x1,y1 in points:
   overlaps = 0

   for x2,y2 in points:
      distance = (((x2-x1)**2) + ((y2-y1)**2))**0.5
      if distance < minimum_distance:
         overlaps += 1
   panel2.plot(x1, y1,
					marker='o',
					markersize=4,
					markeredgewidth=0,
					markeredgecolor='black',
					markerfacecolor=colormap[min(overlaps,100)],
					linewidth=0,
					linestyle='-')
   
# Create new dictionary with type : position
celltypePosDict = {}
for barcode, cell_type in celltypeDict.items():
    if barcode in posDict:
        position = posDict[barcode]
        if cell_type not in celltypePosDict:
            celltypePosDict[cell_type] = [position]
        else:
            celltypePosDict[cell_type].append(position)

# Plot text based on median of positions of cellTypes
medianPos = {}
for cell_type, positions in celltypePosDict.items():
    x = [position[0] for position in positions]
    y = [position[1] for position in positions]
    medianX = np.median(x)
    medianY = np.median(y)
    medianPos[cell_type] = (medianX, medianY)

for cellType, (medianX, medianY) in medianPos.items():
    panel1.text(medianX, medianY, cellType, fontsize=8, path_effects=[pe.withStroke(linewidth=1, foreground="white")], ha='center', va='center')
    
panel2.text(-20.5, -35, 'Density', fontsize = 8, ha='center', va='center') # Density text
panel3.set_yticklabels(['Min','Max']) # Overwrite y_lim

# Dictionary
'''
colorDict = {}
colorDict['monocyte'] = 'red
color = colorDict[cellType]

((array-min(array)) / (max(array))-min(array)))*100

colormap[int(value)]
'''

plt.savefig(outFile, dpi=600)