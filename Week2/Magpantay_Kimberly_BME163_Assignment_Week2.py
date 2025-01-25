# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 2 Assignment
#
# Usage: python3 Magpantay_Kimberly_BME163_Assignment_Week2.py -i BME163_Input_Data_1.txt -o Magpantay_Kimberly_BME163_Assignment_Week2.png
# '''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse
import matplotlib

plt.style.use('BME163') # For stylesheet

# Initialization of sizes of figures
figureWidth = 3
figureHeight = 3

mainPanelWidth = 1.5
mainPanelHeight = 1.5

leftPanelWidth = 0.25
leftPanelHeight = 1.5

topPanelWidth = 1.5
topPanelHeight = 0.25

# Create figure
plt.figure(figsize=(figureWidth,figureHeight))

# Create panels: [left, bottom, width, height]
mainPanel = plt.axes([0.7/figureWidth, 0.3/figureHeight, mainPanelWidth/figureWidth, mainPanelHeight/figureHeight])
leftPanel = plt.axes([0.38/figureWidth, 0.3/figureHeight, leftPanelWidth/figureWidth, leftPanelHeight/figureHeight])
ax = plt.gca()
ax.set_yticks([0, 5, 10, 15]) # Converts to integers
topPanel = plt.axes([0.7/figureWidth, 1.87/figureHeight, topPanelWidth/figureWidth, topPanelHeight/figureHeight])

# Adjust params for panels
mainPanel.tick_params(bottom=True, labelbottom=True, \
                   left=False, labelleft=False, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
leftPanel.tick_params(bottom=True, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
topPanel.tick_params(bottom=False, labelbottom=False, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)

# Parse arguments for input and output files
parser = argparse.ArgumentParser() # A way to get info from your command line
parser.add_argument('--outFile','-o' ,type=str,action='store',default='Magpantay_Kimberly_BME163_Assignment_Week2.png',help='output file')
parser.add_argument('--inFile','-i' ,type=str,action='store',help='input file') # Making use of default to rename output file name
args = parser.parse_args()
outFile=args.outFile
inFile=open(args.inFile)

# Obtain values from data file
xList = []
yList = []

for line in inFile:
  l = line.strip().split()

  x = float(l[1]) # Column 2
  y = float(l[2]) # Column 3

  xList.append(x)
  yList.append(y)

inFile.close()

# Log conversion
xArray = np.log2(np.array(xList)+1) 
yArray = np.log2(np.array(yList)+1)

# Colors
iBlue=(88/255,85/255,120/255)
iYellow=(248/255,174/255,51/255)
iGreen=(120/255,172/255,145/255)

# Top Histogram
bins= np.linspace(0,15,31) # range(0,20,1) # 20 bins, 
xHisto,bins=np.histogram(xArray, bins)

for i in range(0,len(xHisto)-1,1):
	left = bins[i] # Left side of the bin
    
	bottom = 0 # Can be set to 0
    
	width = bins[i+1] - left
    
	height = np.log2(xHisto[i]+1) # Convert height to log
    
	rectangle1=mplpatches.Rectangle((left,bottom),width,height, # (left,bottom),width,height
                                facecolor=iGreen,
                                edgecolor='black',
                                linewidth=0.3) # gives edges
    
	topPanel.add_patch(rectangle1)

# Left Histogram
bins=np.linspace(0,15,31) #range(0,20,1)# 20 bins, from 0 - 100, separated by 5
yHisto,bins=np.histogram(yArray, bins)

for i in range(0,len(yHisto)-1,1):
	left =  0 # Switch bottom
    
	bottom = bins[i] # Switch left
    
	width = np.log2(yHisto[i]+1) # Switch Height
    
	height = (bins[i+1] - bottom) # Switch width
    
	rectangle1=mplpatches.Rectangle((left,bottom),width,height,# (left,bottom),width,height
                                facecolor='grey',
                                edgecolor='black',
                                linewidth=0.3) # gives edges
    
	leftPanel.add_patch(rectangle1)
     

# Main Plot
mainPanel.plot(xArray,yArray,
            marker='o',
            markersize=3, # Marker size 3
            markeredgewidth=0,
            markerfacecolor=iBlue, # Color of points
            linewidth=0,
            alpha = 0.1, # opacity
            linestyle='-')

# Limits
mainPanel.set_xlim(0,15)
mainPanel.set_ylim(0,15)
leftPanel.set_xlim(20,0) # Inverted
leftPanel.set_ylim(0,15)
topPanel.set_xlim(0,15)
topPanel.set_ylim(0,20)

plt.savefig(outFile,dpi=600)
