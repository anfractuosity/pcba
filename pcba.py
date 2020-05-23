#!/usr/bin/python3

"""

    Parses centroid files (.pos files) from KiCad 
    To check component orientation

"""

import os
import argparse
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt

# Graph centroid file and generate output
def graph(centroid,outfile):

    centroid_data = [] # represents centroid data

    with open(centroid) as centroid_input:
    
        line = ""   # line contents
        header = "" # file header
        while (line := centroid_input.readline().strip())[0] == '#':
            header = line.split()[1:]
            continue

        while line:

            lsplit = line.strip().split() # array of columns

            if lsplit[0][0] == '#':
                # at end of file
                break

            line_data = {}
            n = 0
            for col in header:
                try:
                    line_data[col] = float(lsplit[n]) # if data is number
                except:
                    line_data[col] = lsplit[n]        # if data is text
                n += 1

            centroid_data.append(line_data)
            line = centroid_input.readline()

    # Generate centroid graph
    fig, ax = plt.subplots()
    color = 'orange'

    for l in centroid_data:

        if l['Side'] != 'top':
            continue
        
        xp = l['PosX']
        yp = l['PosY']
        tr = matplotlib.transforms.Affine2D().rotate_deg_around(xp,yp,l['Rot'])

        # 0603 sizes
        a = 1.5
        b = 0.8

        if l['Ref'][0] == 'R' or l['Ref'][0] == 'C'  or l['Ref'][0] == 'D' or  l['Ref'][0] == 'L' :
            rect = patches.Rectangle((xp - (a/2),yp - (b/2)),a,b,linewidth=1,edgecolor='b',facecolor='r',transform=tr+ax.transData) #,angle=l['Rot'])
            ax.add_patch(rect)

    ax.scatter([], [], c=color, label=color,
               alpha=0.3, edgecolors='none')
    fig.savefig(outfile)

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="CLI for PCBA centroid parsing")
    parser.add_argument("--input",dest="input", type=str, help="KiCad centroid file",required=True)
    parser.add_argument("--output",dest="output",type=str, help="Image output",required=True)
    args = parser.parse_args()

    # generate graph from centroid file
    graph(os.path.expanduser(args.input),os.path.expanduser(args.output))

