#!/usr/bin/python3

"""

    Parses centroid files (.pos files) from KiCad 
    To check component orientation

"""
import glob
import os
import argparse
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import pcbnew



# Graph centroid file and generate output
def graph(board,centroid,outfile):

    board = pcbnew.LoadBoard(board)
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

    ref = {'R':{"path":"/usr/share/kicad/modules/Resistor_SMD.pretty","colour":"r"},
           'C':{"path":"/usr/share/kicad/modules/Capacitor_SMD.pretty","colour":"b"},
           'L':{"path":"/usr/share/kicad/modules/Inductor_SMD.pretty/","colour":"y"}}

    for mod in board.GetModules(): # Modules(): 'SwigPyObject' object is not iterable; mod is pcbnew.MODULE
        boarddata[mod.GetReference()]  = (mod.GetFootprintRect().GetWidth()/1e6,mod.GetFootprintRect().GetHeight()/1e6)
        if mod.GetReference()[0] in ref:
            fpid = mod.GetFPID()
            footprint = pcbnew.FootprintLoad(ref[mod.GetReference()[0]]['path'], fpid.GetUniStringLibItemName())
            m = pcbnew.MODULE(footprint)
            boarddata[mod.GetReference()]  = (m.GetFootprintRect().GetWidth()/1e6,m.GetFootprintRect().GetHeight()/1e6)
    
    # Generate centroid graph
    fig, ax = plt.subplots()
    color = 'orange'

    for l in centroid_data:

        if l['Side'] != 'top':
            continue
        
        xp = l['PosX']
        yp = l['PosY']
        tr = matplotlib.transforms.Affine2D().rotate_deg_around(xp,yp,l['Rot'])
        a = boarddata[l['Ref']][0]
        b = boarddata[l['Ref']][1]

        if l['Ref'][0] in ref :
            col = ref[l['Ref'][0]]["colour"]
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
    parser.add_argument("--board",dest="board", type=str, help="KiCad board file",required=True)
    parser.add_argument("--output",dest="output",type=str, help="Image output",required=True)
    args = parser.parse_args()

    # generate graph from centroid file
    graph(os.path.expanduser(args.board),os.path.expanduser(args.input),os.path.expanduser(args.output))

