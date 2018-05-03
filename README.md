Problem:

Farm Designer doesn't provide means to create or delete group of plants with one click.
It becomes especially annoying when you want to have many plants of the same kind.

Solution:

This farmware attempts to solve this problem by cloning the "original" plant that you create manually.
You specify the number of rows and columns and the farmware fills the field with (rows x columns -1) copies
of your "original" plant. The spacing between the plants is taken from openfarm database.
If you want to delete automatically created plants - do the same setup but specify "remove" action instead of "add"

Reference:
- integer ORIGINAL PLANT X COORDINATE:    X coordinate of your "original" plant
- integer ORIGINAL PLANT Y COORDINATE:    Y coordinate of your "original" plant
- integer NUMBER OF ROWS:                 desired number of rows, shall be between 0 and 20
- integer NUMBER OF COLUMNS:              desired number of columns, shall be between 0 and 20
- string  WHAT TO DO WITH NEW PLANTS:     action that will be taken on every new plant:
    - "add"     - adds a new plant if there is no plant in these coordinates already
    - "remove"  - removes a plant if found
    - "log"     - just prints info for debug purposes to the log

Installation:

Use this manifest to register farmware
https://raw.githubusercontent.com/etcipnja/Seedalot/master/Seedalot/manifest.json

Bugs:

I noticed that if you change a parameter in WebApplication/Farmware form - you need to place focus on some other
field before you click "RUN". Otherwise old value is  passed to farmware script even though the new value
is displayed in the form.

What is next?

It would be a good idea to add manual override for the spacing between the plants in case if someone doens't like
default vaule from openfarm

Credits:

With the lack of proper documentation about farmware I used this project as a reference point https://github.com/rdegosse/Loop-Plants-With-Filters/blob/master/README.md 

Thank you,
Eugene

