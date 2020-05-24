#!/usr/bin/python3

"""

    Parses centroid files (.pos files) from KiCad 
    To check component orientation

"""
import os
import glob
import argparse
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pcbnew

# Graph centroid file and generate output
def graph(centroid,outfile,libraries):

    # Colours for parts, hardcoded at the mo'
    colours = {'R':"r",
               'C':"b",
               'L':"y",
               'U':"black",
               'Y':"purple",
               'D':"pink",
               'J':"grey",
               'Q':"orange"}

    centroid_data = [] # represents centroid data
    boarddata = {}

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
    
    # Obtain unique packages
    packages = []
    for part in centroid_data:
        packages.append(part['Package'])
    packages = set(packages)

    # Obtain footprint for package
    for package in packages:
        for path in libraries:
            found = False
            for d in glob.glob(path+"/*"):
                footprint = pcbnew.FootprintLoad(d,package)
                if footprint == None:
                    continue
                m = pcbnew.MODULE(footprint)
                boarddata[package]  = (m.GetFootprintRect().GetWidth()/1e6,m.GetFootprintRect().GetHeight()/1e6)
                found = True
                break
            if found:
                break

    # Generate centroid graph
    fig, ax = plt.subplots()
    color = 'orange'

    for l in centroid_data:

        if l['Side'] != 'top':
            continue
        
        xp = l['PosX']
        yp = l['PosY']
        tr = matplotlib.transforms.Affine2D().rotate_deg_around(xp,yp,l['Rot'])

        a = boarddata[l['Package']][0]
        b = boarddata[l['Package']][1]
        col = colours[l['Ref'][0]]
        rect = patches.Rectangle((xp - (a/2),yp - (b/2)),a,b,linewidth=1,edgecolor='b',facecolor=col,transform=tr+ax.transData) #,angle=l['Rot'])
        ax.add_patch(rect)

    ax.scatter([], [], c=color, label=color,
               alpha=0.3, edgecolors='none')
    
    fig.savefig(outfile)
    plt.show()

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="CLI for PCBA centroid parsing")
    parser.add_argument("--input",dest="input", type=str, help="KiCad centroid file",required=True)
    parser.add_argument("--libraries",dest="libraries", type=str, help="KiCad directories that have footprints, comma separated",required=True)
    parser.add_argument("--output",dest="output",type=str, help="Image output",required=True)
    args = parser.parse_args()

    # generate graph from centroid file
    graph(os.path.expanduser(args.input),os.path.expanduser(args.output),args.libraries.split(","))

