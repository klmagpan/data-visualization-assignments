# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 1 Assignment
#
# Usage: python3 Magpantay_Kimberly_BME163_Assignment_Week1.py -o Magpantay_Kimberly_BME163_Assignment_Week1.png
# '''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import numpy as np
import argparse
import matplotlib

plt.style.use('BME163') # For stylesheet

parser = argparse.ArgumentParser()
parser.add_argument('--outFile', '-o', type=str, action='store', help='output file')
args = parser.parse_args()
outFile = args.outFile

# Initialization of sizes of figures
figureWidth = 5
figureHeight = 2

panel1Width = 1
panel2Width = 2
panelHeight = 1

# Create figure
plt.figure(figsize=(figureWidth,figureHeight))

# Create panels: [left, bottom, width, height]
panel1=plt.axes([0.3/figureWidth,0.2/figureHeight,panel1Width/figureWidth,panelHeight/figureHeight])
panel2=plt.axes([2/figureWidth,0.2/figureHeight,panel2Width/figureWidth,panelHeight/figureHeight])

'''Panel 1: Circle'''
# Initialize circle features
radius = 1
diameter = 2 * radius
spacing = diameter - radius
numberOfCircles = 12
xlim = 15
ylim = 16
start = xlim - numberOfCircles - 1

# Set limits of panel1
panel1.set_xlim(0,xlim) # Range of 15
panel1.set_ylim(0,ylim) # Range of 16

# Colors
RB1=(225/255,13/255,50/255)
RB2=(242/255,50/255,54/255)
RB3=(239/255,99/255,59/255)
RB4=(244/255,138/255,30/255)
RB5=(248/255,177/255,61/255)
RB6=(143/255,138/255,86/255)
RB7=(32/255,100/255,113/255)
RB8=(42/255,88/255,132/255)
RB9=(56/255,66/255,156/255)
RB10=(84/255,60/255,135/255)
RB11=(110/255,57/255,115/255)
RB12=(155/255,42/255,90/255)

# Create Circle
for circle in range(numberOfCircles):
	RBColor = locals()[f'RB{circle + 1}'] # Get color from local variable
	color = RBColor
	for i in np.arange(0, np.pi*2, 0.01): # (start, stop, step)
		x = np.sin(i) * radius + (circle * spacing + start) # Puts in middle   
		y = (np.cos(i) * radius) + (ylim / 2) # Puts in middle
		panel1.plot(x,y,
				marker = 'o',
				markersize = 1,
				markeredgewidth = 0,
				markerfacecolor = color,
				linewidth = 0,
				linestyle = '-')

'''Panel 2: Heat Map'''
# Top Heat Map Colors
plasma = [
  (237/255, 252/255, 27/255),
	(245/255, 135/255, 48/255),
	(190/255, 48/255, 101/255),
	(87/255, 0/255, 151/255),
	(15/255, 0/255, 118/255)  
]

# Bottom Heat Map Colors
viridis = [
	(253/255, 231/255, 37/255),
	(94/255, 201/255, 98/255),
	(33/255, 145/255, 140/255),
	(59/255, 82/255, 139/255),
	(68/255, 1/255, 84/255)  
]

# Initialization of Top Panel Arrays (Plasma)
RTop = []
GTop = []
BTop = []
colormapTop = []

for i in range(len(plasma) - 1, 0, -1): # Reverse Order
    color1 = plasma[i]
    color2 = plasma[i - 1]

    # Interpolate between color1 and color2
    R = np.linspace(color1[0], color2[0], 27)
    G = np.linspace(color1[1], color2[1], 27)
    B = np.linspace(color1[2], color2[2], 27)
    RTop = np.concatenate((RTop[:-1], R), axis=None)
    GTop = np.concatenate((GTop[:-1], G), axis=None)
    BTop = np.concatenate((BTop[:-1], B), axis=None)

for index in range(0,101,1):
    colormapTop.append((RTop[index],GTop[index],BTop[index]))
    
# Initialization of Bottom Panel Arrays (Viridis)
RBottom = []
GBottom = []
BBottom = []
colormapBottom = []

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
    colormapBottom.append((RBottom[index],GBottom[index],BBottom[index]))

#                                 (left,bottom),width,height
for index in range(0,101,1):
    rectangleTop=mplpatches.Rectangle((index,50),1,50, # Top Half
                                facecolor=(colormapTop[index]),
                                edgecolor='black',
                                linewidth=0)
    rectangleBottom=mplpatches.Rectangle((index,0),1,50, # Bottom Half
                                facecolor=(colormapBottom[index]),
                                edgecolor='black',
                                linewidth=0) 
    panel2.add_patch(rectangleTop)
    panel2.add_patch(rectangleBottom)
    
panel2.plot([0,100], [50,50], color = 'black', linewidth=0.8) # Plots blakc line in middle

panel2.set_xlim(0,100)
panel2.set_ylim(0,100)
    
# Remove params for both panels
for panel in [panel1,panel2]:
    panel.tick_params(bottom=False, labelbottom=False, \
                   left=False, labelleft=False, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)

plt.savefig(outFile,dpi=600)


# print(matplotlib.get_configdir()) 