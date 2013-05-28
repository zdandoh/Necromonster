This is a very simple map editor that outputs map directories that are
readable by the Necromonster game. There are probably several bugs, but the
editor is quite useable.

Keep all images that you want to use inside the
directory where the main editor script is stored, full paths can be typed,
but these may cause errors on export.

All bounding boxes (links, hitboxes) MUST be drawn from the top left corner
to the bottom right corner. Oddness will ensue if you don't. (Will fix eventually.)

Features:

- loading textures
- moving textures
- placing bounding boxes
- exporting as map directory

Controls:

- Press b to load a background image, this should be done first
- Press a to add surfaces. Enter 1 for a background image (player will be drawn on top). Enter 2 for a foreground image (player will be drawn under).
- Press m while hovering over a surface to move it. Press m again to place.
- Press h to start drawing a new hitbox. Press h again to complete it.
- Press l to start drawing a new link. Press l again to complete it.
- Press e to export the map.