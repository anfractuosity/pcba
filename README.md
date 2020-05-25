# pcba

Parser for KiCad centroid files, that generates a graph to check components are in the right orientation, for PCBA

Usage:

```
./pcba.py --input test.pos --top top.png --bottom bottom.png --libraries mypcb/libs,/usr/share/kicad/modules/
```

# Functionality 

* Colours different components differently
* Indicates pin 1 of component with 'white' blob
* Shows rotation and position of component
