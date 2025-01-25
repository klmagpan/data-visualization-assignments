# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 4 Assignment
#
# Usage: python3 Magpantay_Kimberly_BME163_Assignment_Week4.py -i BME163_Input_Data_4.ident -c BME163_Input_Data_4.cov -o Magpantay_Kimberly_BME163_Assignment_Week4.png
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
parser.add_argument('--identityFile','-i' ,type=str,action='store',default='BME163_Input_Data_4.ident', help='identity file') 
parser.add_argument('--coverageFile','-c' ,type=str,action='store', default='BME163_Input_Data_4.cov',help='celltype file')
args = parser.parse_args()
outFile=args.outFile
identFile=open(args.identityFile)
covFile=open(args.coverageFile)

# Intialize figure sizes
figureHeight=2.5
figureWidth=6
panelWidthCenter=4.5
panelHeightCenter=1.5
relativePanelWidthCenter=panelWidthCenter/figureWidth
relativePanelHeightCenter=panelHeightCenter/figureHeight

# Create Figure
plt.figure(figsize=(figureWidth,figureHeight))

# Create Panels: [left, bottom, width, height] and add axis labels
panelCenter=plt.axes([0.5/figureWidth,0.15,relativePanelWidthCenter,relativePanelHeightCenter])

# Adjust params and labels for panels
panelCenter.tick_params(bottom=False, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
plt.ylabel('Identity (%)')
plt.xlabel('Subread Coverage')
panelCenter.set_ylim(75,100)

# Obtain IDENTITY DATA and put it in dictionary
identDict = {} # Name : identity (%)
for line in identFile: 
	l = line.strip().split()
	name = l[0] # Read names in 1st column
	ident = float(l[1]) # Read identity in 2nd column
	identDict[name] = ident
identFile.close()

# Obtain COVERAGE DATA and put it in dictionary
covDict = {} # Name : Subread Coverage
for line in covFile:
	l = line.strip().split()
	name = l[0]
	cov = float(l[1])
	covDict[name] = cov
covFile.close()

# Initialize Color
iBlue=(44/255,86/255,134/255)
iOrange=(230/255,87/255,43/255)
iYellow=(248/255,174/255,51/255)
iGreen=(32/255,100/255,113/255)

# Initialize category color and data points
categoryColor = {'1-3': iBlue,
			  '4-6': iGreen,
			  '7-9': iYellow,
			  '>=10': iOrange }
categories = {'1-3': [],
			  '4-6': [],
			  '7-9': [],
			  '>=10': [] }

# Organize identities into categories based on coverage data
for name, ident in identDict.items():
	coverage = covDict[name]
	if 1 <= coverage <= 3:
		categories['1-3'].append(ident)
	elif 4 <= coverage <= 6:
		categories['4-6'].append(ident)
	elif 7 <= coverage <= 9:
		categories['7-9'].append(ident)
	elif coverage >= 10:
		categories['>=10'].append(ident)

def swarmplot163 (panel, panelHeight, panelWidth, yList, xPos, xmin, xmax, ymin, ymax, increment, span, color, markersize):
	minimum_distance = markersize/1.5 # Changes swarm distance
	xrange = xmax-xmin
	yrange = ymax-ymin

	possible_positions = []

	for shift in np.arange(0, span, increment):
		possible_positions.append(xPos+shift)
		possible_positions.append(xPos-shift) # Mirrors left side

	plotted_points = []

	for y1 in yList[:500]:
		if len(plotted_points)==0: # Base case
			plotted_points.append((xPos,y1))
		else:
			for x1 in possible_positions:
				distList=[]
				for x2,y2 in plotted_points:
					ydist=((y2-y1)/yrange)*panelHeight
					xdist=((x2-x1)/xrange)*panelWidth
					distance=((xdist**2)+(ydist**2))**(1/2)
					distList.append(distance)
				if min(distList) > minimum_distance:
					plotted_points.append((x1,y1))
					break
			else:
				print(f"{500 - len(plotted_points)} points could not be plotted at position {xPos}.")
				break
	for x1,y1 in plotted_points:
		panel.plot(x1,y1,marker='o',ms=markersize,mew=0,mfc=color,alpha=1,linewidth=0)

# Initialize values
xmin = 0
xmax = 16
ymin = 0
ymax = 100
increment = 0.009 
span = 0.45 
markersize = 2

xPositions = { '1-3': 0.5, '4-6': 1.5, '7-9': 2.5, '>=10': 3.5 } 
for name, identity in categories.items():
	xPos = xPositions[name]
	color = categoryColor[name]
	swarmplot163(panelCenter, panelCenter.get_window_extent().height, panelCenter.get_window_extent().width, identity, xPos, xmin, xmax, ymin, ymax, increment, span, color, markersize)

# Set Labels
panelCenter.set_xticks(list(xPositions.values()))
panelCenter.set_xticklabels(list(xPositions.keys()))

plt.savefig(outFile, dpi=600)