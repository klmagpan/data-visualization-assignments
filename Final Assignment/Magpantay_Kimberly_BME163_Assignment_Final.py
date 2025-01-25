# '''
# Name: Kimberly Magpantay (klmagpan)
# BME163 Spring 2024
# Final Assignment
#
# Usage: python3 Magpantay_Kimberly_BME163_Assignment_Final.py -p5 BME163_Input_Data_5.psl -p6 BME163_Input_Data_6.psl -g gencode.vM12.annotation.gtf -c chr7:45232000-45241000 -o Magpantay_Kimberly_BME163_Assignment_Final.png
# '''

import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
import matplotlib.patheffects as pe
import numpy as np
import matplotlib.image as mpimg
import argparse
import matplotlib
plt.style.use('BME163') # For stylesheet

'''Function to define parse for .psl files'''
def pslParser(pslFile, chromosome, start, end):
    dataList = [] # Returns (readStart, readEnd, list(blockStarts), list(blockWidths), isPlaced)
    for line in pslFile:
        splitLine = line.strip().split('\t')
        readChromosome, readStart, readEnd = splitLine[13], int(splitLine[15]), int(splitLine[16])
        if chromosome == readChromosome:
            keep = False
            if start < readStart < end:
                keep = True
            if start < readEnd < end:
                keep = True
            if readStart < start and readEnd > end:
                keep = True
            if keep:
                blockStarts = np.array(splitLine[20].split(',')[:-1], dtype=int)
                blockWidths = np.array(splitLine[18].split(',')[:-1], dtype=int)
                dataList.append((readStart, readEnd, list(blockStarts), list(blockWidths), False, None))
    return sorted(dataList)

'''Function to plot psl datasets'''
def plotpsl(dataList, panel, colorOfGraph, start, end, linewidth, blockHeight):
    rows = []
    y = 0
    for readStart, readEnd, blockStarts, blockWidths, placed, blockTypes in dataList:
        placed_in_row = False
        for row in rows:
            if readStart > row[-1][1]:  # If current read starts after the last read in this row ends
                row.append((readStart, readEnd, blockStarts, blockWidths, blockTypes))
                placed_in_row = True
                break
        if not placed_in_row:
            rows.append([(readStart, readEnd, blockStarts, blockWidths, blockTypes)])  # Start a new row
    for row in rows:
        for readStart, readEnd, blockStarts, blockWidths, blockTypes in row:
            rectangle = mplpatches.Rectangle([readStart, y], readEnd - readStart, 0.05,
                                             facecolor=colorOfGraph,
                                             edgecolor=colorOfGraph,
                                             linewidth=linewidth)
            panel.add_patch(rectangle)
            for j in range(len(blockStarts)):
                blockStart = blockStarts[j]
                blockWidth = blockWidths[j]
                if blockTypes == None:
                    rectangle = mplpatches.Rectangle([blockStart, y + 0.2], blockWidth, blockHeight,
													facecolor=colorOfGraph,
													edgecolor='black',
													linewidth=linewidth)
                    panel.add_patch(rectangle)
                    
        y += 1
    panel.set_xlim(start, end)
    panel.set_ylim(0, y+5) # Set limit higher to match assignment template

'''Function to plot gtf datasets'''
def plotgtf(dataList, panel, colorOfGraph, start, end, linewidth, blockHeight):
     y = 0
     rows = []
     for readStarts, readEnds, blockStarts, blockWidths, placed, blockTypes in sorted(dataList):
        placed_in_row = False
        for row in rows:
            if readStarts > row[-1][1]:  # If current read starts after the last read in this row ends
                row.append((readStarts, readEnds, blockStarts, blockWidths, placed, blockTypes))
                placed_in_row = True
                break
        if not placed_in_row:
            rows.append([(readStarts, readEnds, blockStarts, blockWidths, placed, blockTypes)])
     for row in rows:
     	for readStart, readEnd, blockStarts, blockWidths, placed, blockTypes in row: #sorted(dataList):
          rectangle = mplpatches.Rectangle([readStart,y+0.2],readEnd-readStart,0.05,
													facecolor=colorOfGraph,
													edgecolor='black',
													linewidth=linewidth)
          panel.add_patch(rectangle)
          for i in range(0, len(blockStarts)): 
               blockStart = blockStarts[i]
               blockWidth=blockWidths[i]
               blockType = blockTypes[i]
               if blockType == 'exon':
                    rectangle = mplpatches.Rectangle([blockStart,y+0.1],blockWidth,0.25,
															facecolor=colorOfGraph,
															edgecolor='black',
															linewidth=linewidth)
                    panel.add_patch(rectangle)
               if blockType == 'CDS':
                    rectangle = mplpatches.Rectangle([blockStart,y],blockWidth,0.5,
															facecolor=colorOfGraph,
															edgecolor='black',
															linewidth=linewidth)
                    panel.add_patch(rectangle)
          y += 1
     panel.set_xlim(start,end)
     panel.set_ylim(0,y+1)

'''Function to parse .gtf files'''     
def gtfParser(gtfFile, chromosome, start, end):
    gtfDict = {}
    for line in gtfFile:
         if not line.startswith('#'):
               splitLine=line.strip().split('\t')
               if splitLine[2]=='exon' or splitLine[2]=='CDS':
                    Gchromosome=splitLine[0]
                    Gstart,Gend,Gfeature=int(splitLine[3]),int(splitLine[4]),splitLine[2]
                    info=splitLine[8]
                    transcript_id=info.split('transcript_id ')[1].split(';')[0].strip('"')
					# print(chromosome,start,end,feature,transcript_id)
                    if transcript_id not in gtfDict:
                         gtfDict[transcript_id] = []
                    gtfDict[transcript_id].append((Gchromosome,Gstart,Gend,Gfeature))
    gtfList=[]
    for transcript_id,features in gtfDict.items():
            startsNends=[]
            blockStarts=[]
            blockWidths=[]
            blockTypes=[]
            for Gchromosome,Gstart,Gend,type1 in features:
                        startsNends.append(Gstart)
                        startsNends.append(Gend)
                        blockStarts.append(Gstart)
                        blockWidths.append(Gend-Gstart)
                        blockTypes.append(type1)
            readStart=min(startsNends)
            readEnd=max(startsNends)
            if chromosome == Gchromosome:
                        keep = False
                        if start < Gstart < end: # If readStart is between the start/end coordinates
                                keep = True
                        if start < Gend  < end: # If readEnd if between start/end
                               keep = True
                        if Gstart<start and Gend>end:
                               keep = True
                        if keep == True:
                              gtfList.append([readStart,readEnd,list(blockStarts),list(blockWidths),False,blockTypes])
    return gtfList

def main():
      
      '''Color'''
      iOrange=(230/255,87/255,43/255) #sorted by end [2]
      iBlue=(88/255,85/255,120/255) # 0.05 #sorted by start # [3/4
      grey = 'Grey' # 0.25, sorted by start. [1]
      
      '''Parse Arguments for Input and Output Files'''
      parser = argparse.ArgumentParser() # A way to get info from your command line
      parser.add_argument('--outFile','-o' ,type=str,action='store',default='output.png',help='output file')
      parser.add_argument('--p5File','-p5' ,type=str,action='store',default='BME163_Input_Data_5.psl', help='p5 file')
      parser.add_argument('--p6File','-p6' ,type=str,action='store',default='BME163_Input_Data_6.psl', help='p6 file')  
      parser.add_argument('--gencodeFile','-g', type=str, action='store', default='gencode.vM12.annotation.gtf', help='gencodeFile')
      parser.add_argument('--geneLocus','-c', type=str, action='store', default='', help='geneLocus')
      args = parser.parse_args()
      outFile=args.outFile
      p5File=open(args.p5File)
      p6File=open(args.p6File)
      gencodeFile=open(args.gencodeFile)
      geneLocus = args.geneLocus
      
      '''Split String'''
      chromosome, positions = geneLocus.split(":") # chromosome: chr#
      left, right = positions.split("-")
      start = int(left) # left: int(#)
      end = int(right) # right: int(#)
      
      '''Parse files'''
      p5Dataset = pslParser(p5File, chromosome, start, end)
      p6Dataset = pslParser(p6File, chromosome, start, end)
      gtfDataset = gtfParser(gencodeFile, chromosome, start, end)

      
      '''Close files'''
      p5File.close()
      p6File.close()
      gencodeFile.close()
      
      '''Initialize Panels'''
      figureHeight = 6
      figureHeight=6
      figureWidth=5
      fig_1 = plt.figure(figsize=(figureWidth,figureHeight))
      panel0 = plt.axes([0.1/figureWidth, 0.1/figureHeight , 4/figureWidth , 0.4/figureHeight],frameon=True)
      panel1 = plt.axes([0.1/figureWidth, 0.5/figureHeight , 4/figureWidth , 1.5/figureHeight],frameon=True)
      panel2 = plt.axes([0.1/figureWidth, 2.2/figureHeight , 4/figureWidth , 1.5/figureHeight],frameon=True)
      panel3 = plt.axes([0.1/figureWidth, 3.9/figureHeight , 4/figureWidth , 1.5/figureHeight],frameon=True)
      for panel in [panel0, panel1, panel2, panel3]:
            panel.tick_params(bottom=False, labelbottom=False, \
						left=False, labelleft=False, \
						right=False, labelright=False, \
	  					top=False, labeltop=False)
            
      '''Plot Graphs'''        
      plotpsl(sorted(p5Dataset, key=lambda x:x[1]), panel2, iOrange, start, end, 0, 0.5) # Reverse
      plotpsl(sorted(p6Dataset), panel1, iBlue, start, end, 0.05, 0.5)
      plotgtf(sorted(gtfDataset), panel3, grey, start, end, 0.25, 0.1)

      '''Save Figure'''
      plt.savefig(outFile, dpi=2400)

    
main()


	

