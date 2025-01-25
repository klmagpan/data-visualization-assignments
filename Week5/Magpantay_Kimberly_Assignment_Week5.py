# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Week 4 Assignment
#
# Usage: python3 Magpantay_Kimberly_Assignment_Week5.py -s Splice_Sequences.fasta -A A.png -T T.png -G G.png -C C.png -o Magpantay_Kimberly_Assignment_Week5.png
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
parser.add_argument('--A','-A' ,type=str,action='store',default='A.png', help='A file')
parser.add_argument('--T','-T' ,type=str,action='store',default='T.png', help='T file') 
parser.add_argument('--G','-G' ,type=str,action='store',default='G.png', help='G file') 
parser.add_argument('--C','-C' ,type=str,action='store',default='C.png', help='C file')  
parser.add_argument('--fastaFile','-s' ,type=str,action='store',default='Splice_Sequences.fasta', help='fasta file') 

args = parser.parse_args()
outFile=args.outFile
fastaFile=args.fastaFile

# Use the image files provided in Assignment Data on Canvas 
A=mpimg.imread('A.png')
G=mpimg.imread('G.png')
C=mpimg.imread('C.png')
T=mpimg.imread('T.png')

# Initialize Figure Sizes
figureWidth = 5
figureHeight = 2
panelWidth=1.5
panelHeight = 0.5

# Create Figure
fig_1 = plt.figure(figsize=(figureWidth,figureHeight))

# Create Panels: [left, bottom, width, height] and add axis labels
panel1 = plt.axes([0.5/figureWidth , 0.3 , panelWidth/figureWidth , panelHeight/figureHeight],frameon=True)
plt.title("5'SS")
plt.xlabel('Distance to\nSplice Site')
plt.ylabel('Bits')
panel2 = plt.axes([2.2/figureWidth , 0.3 , panelWidth/figureWidth , panelHeight/figureHeight],frameon=True)
plt.xlabel('Distance to\nSplice Site')

# Adjust params and labels for panels
for panel in [panel1, panel2]:
	panel.set_ylim(0,2)
	panel.set_xlim(-10,10)
	panel.plot([0,0], [0,2], color = 'black', linewidth=0.4) # Plots blakc line in middle

panel1.tick_params(bottom=True, labelbottom=True, \
                   left=True, labelleft=True, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)
plt.title("3'SS")
panel2.tick_params(bottom=True, labelbottom=True, \
                   left=False, labelleft=False, \
                   right=False, labelright=False, \
                   top=False, labeltop=False)

'''Fasta Reader File'''
def fastaReader(fasta):
  reads = {}
  header = ''
  with open(fasta) as fa:
    for line in fa:
      l = line.strip()
      if l[0] == '>':
        if header in reads:
          reads[header] = ''.join(reads[header])
        if l[1:] not in reads:
          header = l[1:]
          reads[header] = []
      else:
        reads[header].append(l)
    reads[header] = ''.join(reads[header])
    return reads

# Read from Fastafile
reads = fastaReader(fastaFile)

print(reads)
# Initialize dictionaries
array3Dict = {i: [] for i in range(20)}
array5Dict = {i: [] for i in range(20)}

# Fill dictionaries based on sequence name
for name, seq in reads.items():
    if "5'" in name:
        for pos, base in enumerate(seq):
            array5Dict[pos].append(base)
    elif "3'" in name:
        for pos, base in enumerate(seq):
            array3Dict[pos].append(base)
    
images = {'A': A, 'T': T, 'C': C, 'G': G}

def calculationPlot(freqDict, panel, image_dict):
    for base in freqDict.keys(): 
        frequencies = {}
        total_bases = len(freqDict[base])
        
        for b in freqDict[base]:
            frequencies[b] = frequencies.get(b, 0) + 1 # Increments count of base
        
        H = 0
    
        for count in frequencies.values(): # Iterates over the counts of the bases
            average = count / total_bases # Calculates count by the total number of bases
            H -= average * np.log2(average)
        R = 2 - H # Calculate R 

        height = 0
        for key in sorted(frequencies, key=lambda x: frequencies[x]):
            if H > 0.2:
                value = frequencies[key]
                average = value / total_bases
                panel.imshow(image_dict[key], extent=[base - 10, base - 9, height, height + (average * R)], aspect='auto')
                height += average * R

calculationPlot(array5Dict, panel1, images)
calculationPlot(array3Dict, panel2, images)

plt.savefig(outFile, dpi=600)