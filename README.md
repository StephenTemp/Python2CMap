# Python2CMap
Description: Trying to figure out and manipulate CMap

## Understanding CMap Functions

## MAIN FUNCTIONS (PLOTTING)

### regionalMap()
  Takes in:

    * list of tables to map with parallel list of variables
    * start and end dates
    * range of latitude and longitude data
    * range of depths
    * fname (usually set to 'regional')
    * exportDataFlag (whether the map should be exported or not)

  Retrieves desired data from mySQL database and feeds data into **structuredMap()** to reformat, feeding reformatted data into **bokehMap()** for graphing/mapping. Maps data primarily using lat and lon values onto the world map.

### timeSeries()
  Takes in:

    * list of tables to map with parallel list of variables
    * start and end dates
    * range of latitude and longitude data
    * range of depths
    * fname (usually set to 'regional')
    * exportDataFlag (whether the map should be exported or not)

    Retrieves data from helper method but otherwise does all operations itself (no **structuredMap**, **bokehMap**). Plots graphs based primarily on time values (mapping to the given variable).

### histogram()
  Takes in: same as above (most of these functions do)

  Creates a histogram plotting the 'density' of specific values from your variables dataset. Worried this one may be less stable due to some reformatting with the **depth** dimension, but it hasn't crashed on me yet and I've tried out the majority of **depth** values
## ------------------------------------------

### structuredMap()
  Takes in:

    * DateFrame (consisting of longs, lats, variable   being measured, and  times)
    * Table name
    * Variable name

  Creates lists of unique latitudes, longitudes, and time values

  Creates list of variable values and reshapes to mirror long/lat values

  Returns:

      * reshaped variable, long, lat arrays
      * subject of intended map: "variable + unit + time"
      * variable and table name

### bokehMap()
  Takes in:

    * data (variable values), lat, long arrays
    * subject string ("variable + unit + time")
    * fname (always seems to be set to regional)
    * table and variable lists

  Constructs and displays the map

### getUnit()
  Takes in:

    * table and variable names

  Returns:

    * the variable's unit of measurement
