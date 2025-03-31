This is code for figuring out the nearest gold, silver, etc. if someone casts
Seek Earth or Seek Magic in a GURPS game.

Prerequisites:

* You need all the maps you care about in Foundry.
* Each map should have a single elevation.  If you put all the levels of a
  tower on one map instead of multiple maps, this code won't work well
  without modification.


Steps:

1. Make sure all Foundry maps have room labels, which are text drawings that
   start with a number.  (So "3", "3a", and "47" are room labels.  "Down" and
   "T" are not.)

2. In Foundry, as the Gamemaster user, set room_labels_xy.js as a script macro
   on a function key.

3. Run room_labels_xy.js on all the maps you care about.  Each time you run it
   it should open a new browser tab with a text blob containing lines like
   "map name: room number: x,y"
   Paste all these blobs into a single text file called rooms.txt

4. Create a file called treasures.txt where each line contains a global room
   number (level prefix, hyphen, room number), a colon, and then a comma-separated
   list of the detectable treasure types found in that room.
   "1-2A: copper, silver, gold"

5. Create a file called map_prefix.txt
   Each line should have the full Foundry name of a map (as seen in the first
   column of rooms.txt), a colon, and then the level prefix you use before the
   hyphen in the treasures.txt file.
   "Arden_Vul_Ruins: AV"
   This is needed because sometimes one level in the dungeon key needs to be
   split up into multiple maps in Foundry for efficiency.  So if level 3 of
   your dungeon ends up being "level3_east" and "level3_west" maps, both of
   those entries would map to "3".

6. Create a file called map_xyz.txt
   This will let you convert each map's local x and y coordinates (in pixels)
   to your game world's global x, y, and z coordinates (in yards).
   Each line in this file is map name, x0, y0, z, x_scale, y_scale
   x0 is the world global x coordinate of the left side of this map
   y0 is the world global y coordinate of the top edge of this map
   z is the elevation of this map.  (Each map only has one elevation.)
   x_scale and y_scale are the scale of this map, in yards per pixel

7. Run the program.  Something like:
python3 seekearth.py -t treasures.txt -p map_prefix.txt -x map_xyz.txt -r rooms.txt -f gold -s 3-1 -n 10

This is saying to use treasures.txt, map_prefix_txt, map_xyz.txt, and rooms.txt
as the data files, search for "gold", start from room 3-1, and return the 10
closest results.

The program will find the nearest treasures of the requested type, and spit out
distance and direction (for the player) as well as the room number (for the
GM).


FAQ:

Q. I don't use Foundry.  Can you read the room numbers and their x,y locations
   off my map images?

A. I tried this, but none of the OCR software I tried was good enough to get
   most of the room numbers off my dungeon map images.  If you have maps where
   OCR actually works, feel free to write a script that outputs room numbers
   and their (x,y) pixel coordinates to a rooms.txt file, and the rest should
   work.
