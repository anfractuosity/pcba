# pcba

Parser for KiCad centroid files, that generates a graph to check components are in the right orientation, for PCBA

Usage:

```
./pcba.py --input test.pos --output out.png --libraries mypcb/libs,/usr/share/kicad/modules/
```

# To Do

* Need to make colours autogenerate?
* Need to make work for bottom of board too
* See if it's possible to mark pin number 1 of components
