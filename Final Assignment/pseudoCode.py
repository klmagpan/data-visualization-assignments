'''
Each line place the first read and decide if the next read
has room next to it. If not, ignore reads until get a read whose start is bigger than the end
of the read you previously plotted. 


for row in arbitrary_number:
	previous_end=-1
	for read in all_reads:
		if the the read does not already have a y position (only consider the reads that haven't been "placed" yet [boolean])
		is the readstart bigger than the end of the previously plotted read
			assign read to this row
			reset previously_end based on current read

Another way to be written:

read = (start, end, blockstart, blockwidths, 2) (mainly just care about start and end)
											Boolean determines if read does/doesn't already have a y position
for row in len(all_reads):
	previous_end = -1
	for read in all_reads:
		if the read does has a y position that is 0:
			if the read start is bigger than the end of the previously plotted read
				assign read to this row
				
'''

# def pslParser(pslFile, colorGraph, panel):
# 	y = 0
# 	dataList = []
# 	for line in pslFile:
# 		splitLine = line.strip().split('\t')
# 		readChromosome, readStart, readEnd = splitLine[13], int(splitLine[15]), int(splitLine[16]) # Column 14 = how many bases long
# 		if chromosome == readChromosome:
# 			keep = False
# 			if start < readStart < end: # If readStart is between the start/end coordinates
# 				keep = True
# 			if start < readEnd  < end: # If readEnd if between start/end
# 				keep = True
# 			if readStart<start and readEnd>end:
# 				keep = True
# 			if keep:
# 				blockStarts = np.array(splitLine[20].split(',')[:-1], dtype=int) # In gene, this is where the block starts
# 				blockWidths = np.array(splitLine[18].split(',')[:-1], dtype=int) # Splices the last string b/c trailing comma
# 				dataList.append((readStart,readEnd,list(blockStarts),list(blockWidths)))
# 	for readStart, readEnd, blockStarts, blockWidths in sorted(dataList): # Plot rectangle that goes from its start to its end
# 		rectangle = mplpatches.Rectangle([readStart,y+0.2],readEnd-readStart,0.1,
# 													facecolor=colorGraph,
# 													edgecolor='black',
# 													linewidth=0)
# 		panel.add_patch(rectangle)
# 		for i in range(0, len(blockStarts),1): # Loop over blocks starts (wide rectangles)
# 			blockStart = blockStarts[i]
# 			blockWidth=blockWidths[i]
# 			rectangle = mplpatches.Rectangle([blockStart,y],blockWidth,0.5,
# 													facecolor=colorGraph,
# 													edgecolor='black',
# 													linewidth=0)
# 			panel.add_patch(rectangle)
# 		y += 1
# 	panel.set_xlim(start,end)
# 	panel.set_ylim(0,y+1)

'''Function to define parser for .psl files'''
# def pslParser(pslFile, colorGraph, panel):
#     dataList = []
#     y = 0
#     for line in pslFile:
#         splitLine = line.strip().split('\t')
#         readChromosome, readStart, readEnd = splitLine[13], int(splitLine[15]), int(splitLine[16])
#         if chromosome == readChromosome:
#             keep = False
#             if start < readStart < end:
#                 keep = True
#             if start < readEnd < end:
#                 keep = True
#             if readStart < start and readEnd > end:
#                 keep = True
#             if keep:
#                 blockStarts = np.array(splitLine[20].split(',')[:-1], dtype=int)
#                 blockWidths = np.array(splitLine[18].split(',')[:-1], dtype=int)
#                 dataList.append((readStart, readEnd, list(blockStarts), list(blockWidths), False))
    
    # rows = []
    
    # for readStart, readEnd, blockStarts, blockWidths, placed in sorted(dataList):
    #     placed_in_row = False
    #     for row in rows:
    #         if readStart > row[-1][1]:  # If current read starts after the last read in this row ends
    #             row.append((readStart, readEnd, blockStarts, blockWidths))
    #             placed_in_row = True
    #             break
    #     if not placed_in_row:
    #         rows.append([(readStart, readEnd, blockStarts, blockWidths)])  # Start a new row
    # for row in rows:
    #     for readStart, readEnd, blockStarts, blockWidths in row:
    #         rectangle = mplpatches.Rectangle([readStart, y + 0.2], readEnd - readStart, 0.1,
    #                                          facecolor=colorGraph,
    #                                          edgecolor='black',
    #                                          linewidth=0)
    #         panel.add_patch(rectangle)
    #         for j in range(len(blockStarts)):
    #             blockStart = blockStarts[j]
    #             blockWidth = blockWidths[j]
    #             rectangle = mplpatches.Rectangle([blockStart, y], blockWidth, 0.5,
    #                                              facecolor=colorGraph,
    #                                              edgecolor='black',
    #                                              linewidth=0)
    #             panel.add_patch(rectangle)
    #     y += 1
    
    # panel.set_xlim(start, end)
    # panel.set_ylim(0, y + 1)

'''
Find the smallest start of the elements and the highest end of the elements
Blockstarts: (first number of each array)
Blockwidths: 

def main():
	# Set up your figure
	psl5=readPsl(p5)
	psl6=readPsl9p(p6)
	gtf=readGTF9(g)
	plotStuff(ps5,panel#)
	plotStuff(ps6,panel#)
	plotStuff(gtf,panel#)

	# Set up panel characteristics (limits, xticks, labels)
	Save figure
'''


'''
# Start of 3 > end
# Move read 3 down
# Start of 4 is smaller than the end of 3, so can't plot
# For y position in a range from zero to however high could possibly go (length of the reads)
# For each line, just check and place
# In list of reads, want to have Boolean that tells whether read is placed or not (If true, don't look at anymore)

Each line place the first read and decide if the next read
has room next to it. If not, ignore reads until get a read whose start is bigger than the end
of the read you previously plotted. 


for row in arbitrary_number:
	previous_end=-1
	for read in all_reads:
		if the the read does not already have a y position (only consider the reads that haven't been "placed" yet [boolean])
		is the readstart bigger than the end of the previously plotted read
			assign read to this row
			reset previously_end based on current read

Another way to be written:

read = (start, end, blockstart, blockwidths, 2) (mainly just care about start and end)
											Boolean determines if read does/doesn't already have a y position
for row in len(all_reads):
	previous_end = -1
	for read in all_reads:
		if the read does has a y position that is 0:
			if the read start is bigger than the end of the previously plotted read
				assign read to this row
'''

'''
GTF file


'''


# y = 0
# dataList = []
# for line in p5File:
# 	splitLine = line.strip().split('\t')
# 	readChromosome, readStart, readEnd = splitLine[13], int(splitLine[15]), int(splitLine[16])
# 	if chromosome == readChromosome:
# 		keep = False
# 		if start < readStart < end:
# 			keep = True
# 		if start < readEnd  < end:
# 			keep = True
# 		if readStart<start and readEnd>end:
# 			keep = True
# 		if keep:
# 			blockStarts = np.array(splitLine[20].split(',')[:-1], dtype=int) # In gene, this is where the block starts
# 			blockWidths = np.array(splitLine[18].split(',')[:-1], dtype=int)
# 			dataList.append((readStart,readEnd,list(blockStarts),list(blockWidths)))

# for readStart, readEnd, blockStarts, blockWidths in dataList:
# 	rectangle = mplpatches.Rectangle([readStart,y+0.2],readEnd-readStart,0.1,
# 												facecolor='grey',
# 												edgecolor='black',
# 												linewidth=0)
# 	panel1.add_patch(rectangle)
# 	for i in range(0, len(blockStarts),1):
# 		blockStart = blockStarts[i]
# 		blockWidth=blockWidths[i]
# 		rectangle = mplpatches.Rectangle([blockStart,y],blockWidth,0.5,
# 												facecolor='grey',
# 												edgecolor='black',
# 												linewidth=0)
# 		panel1.add_patch(rectangle)
# 	y += 1
# panel1.set_xlim(start,end)
# panel1.set_ylim(0,y+1)

'''
Instructions
- For each panel, y 

- Exons = Rectangles
	- In order, but can skip exons [Exon 1, Exon 3] instead of [Exon 1, Exon 2, Exon 3]
	- Thick = CDS
- Introns = Lines

- Read GTF file
	- Second column: gene, transcript (connected to gene ID and transcript ID)
		- Collect all the parts associated with one transcript
			- Transcripts might have multiple exons 

		- One CDS field for one exon that it's overlapping with 
	-  Collect every line that has the same transcript ID, use it as a key in a dictionary, and collect every single element

- Read PSL file
	- Says where to plot and its lengths
	- What chromosome it's aligned to and where it starts/ends
	- Start end, --> Broken up into 1+ blocks (bases long or width)--> Each block at the start of last column numbers

- Top: Genome annotations from gtf file
- Bottom two files: from psl file
- Only care about things that overlaps with "this" window
'''

	# 	# print(min(startsNends),max(startsNends))
	# 	if chromosome == Gchromosome:
	# 			keep = False
	# 			if start < Gstart < end: # If readStart is between the start/end coordinates
	# 				keep = True
	# 			if start < Gend  < end: # If readEnd if between start/end
	# 				keep = True
	# 			if Gstart<start and Gend>end:
	# 				keep = True
	# 			if keep == True:
	# 				gtfList.append([Gstart,Gend,blockStarts,blockWidths,blockTypes,0])
                        
			
	# # for entry in gtfList:
	# # 	print(entry)