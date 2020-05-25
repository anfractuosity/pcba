#!/usr/bin/python3

"""

    Parses centroid files (.pos files) from KiCad 
    To check component orientation

"""
import re
import os
import glob
import argparse
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pcbnew

# Get reference name, without number ID hopefully
def getref(ref):
    comp = re.match("(.*?)[0-9]+$", ref)
    if comp != None:
        return comp.group(1)
    else:
        return ref


# Generate graph with components for particular side of the board
def image(refs, colours, centroid_data, boarddata, side, output):

    # Generate centroid graph
    fig, ax = plt.subplots()

    for l in centroid_data:

        # Display components for this side of board
        if l["Side"] != side:
            continue

        # If component package not found, ignore
        if l["Package"] not in boarddata:
            print("Not found ",l["Package"])
            continue

        xp = l["PosX"]
        yp = l["PosY"]
        tr = matplotlib.transforms.Affine2D().rotate_deg_around(xp, yp, l["Rot"])
        a = boarddata[l["Package"]]["size"][0]
        b = boarddata[l["Package"]]["size"][1]
        z = 0.5
        comp = getref(l["Ref"])
        col = colours[comp]

        # Adjust x,y pos of component if centre isn't 0,0
        if "centre" in boarddata[l["Package"]]:
            centre = boarddata[l["Package"]]["centre"]
            xp += centre[0]
            yp -= centre[1]

        # Generate rectangle for component
        rect = patches.Rectangle(
            (xp - (a / 2), yp - (b / 2)),
            a,
            b,
            linewidth=1,
            edgecolor="b",
            facecolor=col,
        )

        # If we found pin 1, display it depending if we're on the top/bottom of board
        if "pin" in boarddata[l["Package"]]:
            if l["Side"] == "top":
                pin1 = patches.Rectangle(
                    (
                        xp + boarddata[l["Package"]]["pin"][0] - (z / 2),
                        yp - boarddata[l["Package"]]["pin"][1] - (z / 2),
                    ),
                    z,
                    z,
                    facecolor="white",
                )
            else:
                pin1 = patches.Rectangle(
                    (
                        xp - boarddata[l["Package"]]["pin"][0] - (z / 2),
                        yp + boarddata[l["Package"]]["pin"][1] - (z / 2),
                    ),
                    z,
                    z,
                    facecolor="white",
                )
            dat = [rect, pin1]
        else:
            dat = [rect]

        collection = matplotlib.collections.PatchCollection(dat, match_original=True)
        collection.set_transform(tr + ax.transData)
        ax.add_collection(collection)
        ax.text(
            xp, yp, l["Ref"], fontsize=7, fontweight="bold", transform=tr + ax.transData
        )

    ax.scatter([], [])

    # Display legend for colours
    compcolour = []
    refcolour = []
    for r in refs:
        compcolour.append(Line2D([0], [0], color=colours[r], lw=4))
        refcolour.append(r)
    ax.legend(compcolour, refcolour)

    plt.show()
    fig.savefig(output)


# Attempt to load footprint for package
def load(path, package):

    footprint = pcbnew.FootprintLoad(path, package)
    data = {}

    if footprint != None:
        m = pcbnew.MODULE(footprint)
        # Find pin 1
        pads = m.Pads()
        pinv = None
        pinno = "1"
        for p in pads:
            if p.GetName() == pinno:
                pinv = p.GetPosition()
                break

        centre = (
            m.GetFootprintRect().GetCenter()[0] / 1e6,
            m.GetFootprintRect().GetCenter()[1] / 1e6,
        )
        data = {
            "centre": centre,
            "size": (
                m.GetFootprintRect().GetWidth() / 1e6,
                m.GetFootprintRect().GetHeight() / 1e6,
            ),
        }
        if pinv is not None:
            data["pin"] = (pinv[0] / 1e6, pinv[1] / 1e6)

    return data


# Used to escape from loops
class GetOutOfLoop(Exception):
    pass


# Graph centroid file and generate output
def graph(centroid, libraries, top, bottom=""):

    centroid_data = []  # represents centroid data
    boarddata = {}

    with open(centroid) as centroid_input:

        line = ""  # line contents
        header = ""  # file header
        while (line := centroid_input.readline())[0] == "#":
            header = line.split()[1:]
            continue

        while line:

            if line[0] == " ":
                line = centroid_input.readline()
                continue

            lsplit = line.strip().split()  # array of columns

            if line.strip() == "## End":   # At end of file
                break

            line_data = {}
            n = 0
            for col in header:
                try:
                    line_data[col] = float(lsplit[n])  # if data is number
                except:
                    line_data[col] = lsplit[n]  # if data is text
                n += 1

            centroid_data.append(line_data)
            line = centroid_input.readline()

    # Obtain unique packages
    refs = []
    packages = []
    for part in centroid_data:
        packages.append(part["Package"])
        comp = getref(part["Ref"])
        refs.append(comp)

    packages = set(packages)
    refs = set(refs)

    # Generate colours programatically
    colours = {}
    colour_list = plt.cm.tab20(np.linspace(0, 1, len(refs)))
    ccount = 0
    for r in refs:
        colours[r] = colour_list[ccount]
        ccount += 1

    # Obtain footprint for package
    for package in packages:
        try:

            for path in libraries:
                path = os.path.expanduser(path)
                data = load(path, package)
                if data != {}:
                    boarddata[package] = data
                    raise GetOutOfLoop

            for path in libraries:
                for d in glob.glob(path + "/*/"):
                    data = load(d, package)
                    if data != {}:
                        boarddata[package] = data
                        raise GetOutOfLoop

        except GetOutOfLoop:
            outtahere = True

    image(refs, colours, centroid_data, boarddata, "top", top)

    if bottom != "":
        image(refs, colours, centroid_data, boarddata, "bottom", bottom)


if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description="CLI for PCBA centroid parsing")
    parser.add_argument(
        "--input", dest="input", type=str, help="KiCad centroid file", required=True
    )
    parser.add_argument(
        "--libraries",
        dest="libraries",
        type=str,
        help="KiCad directories that have footprints, comma separated",
        required=True,
    )
    parser.add_argument(
        "--top", dest="top", type=str, help="Image output for top", required=True
    )
    parser.add_argument(
        "--bottom",
        dest="bottom",
        type=str,
        help="Image output for bottom",
        required=False,
    )
    args = parser.parse_args()

    # generate graph from centroid file
    if not args.bottom:
        graph(
            os.path.expanduser(args.input),
            os.path.expanduser(args.top),
            args.libraries.split(","),
            top=os.path.expanduser(args.top),
        )
    else:
        graph(
            os.path.expanduser(args.input),
            args.libraries.split(","),
            top=os.path.expanduser(args.top),
            bottom=os.path.expanduser(args.bottom),
        )
