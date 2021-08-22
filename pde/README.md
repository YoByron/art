## How to run Processing sketches with VSCode

Use the Processing VSCode extension by Luke-zhang-04.
Make sure that processing-java is on the $PATH. On Linux, add
its folder to the .bash_profile like this:
export PATH="$PATH:/home/sebastian/Processing/processing-4.0b1"
Of course, adjust the folder path for your version.

Run a sketch with
processing-java --sketch=path/to/sketch/folder --run
or use the command from the VSCode extension. Or just make
a keyboard shortcut for that.
Use "editorFocus && editorLangId == 'pde'" for the "when" field
and remove all conflicting shortcuts.

The sketch folder must contain a .pde file with the same name in order to be a valid sketch.
