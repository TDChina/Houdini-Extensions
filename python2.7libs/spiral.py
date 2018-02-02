# Copyright (c) 2018 ChuckBiBi

import hou
from math import sin, cos


def create_spiral():
    geoNet = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    spiral = geoNet.pwd().createNode("curve")

    coordsParm = spiral.parm("coords")
    typeParm = spiral.parm("type")

    input = hou.ui.readMultiInput(message="Input Parms:",
                                  input_labels=["height", "upRadius",
                                                "underRadius", "frequency"],
                                  initial_contents=["40", "0", "30", "3"])

    height = float(input[1][0])
    upRadius = float(input[1][1])
    underRadius = float(input[1][2])
    frequency = float(input[1][3])

    coordsStr = ""
    radius = underRadius
    step = (underRadius - upRadius) / (height * frequency)

    for i in range(int(height * frequency)):
        px = str(radius * sin(i))
        py = str(i * 1 / frequency)
        pz = str(radius * cos(i))

        coordsStr += px + "," + py + "," + pz + " "
        radius -= step

    coordsParm.set(coordsStr)
    typeParm.set("nurbs")
