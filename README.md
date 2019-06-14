# Python2CMap
Description: Trying to figure out and manipulate CMap

## Understanding CMap Functions

### regionalMap()
  Takes in:
    -list of tables to map with parallel list of variables
    -start and end dates
    -range of latitude and longitude data
    -range of depths
    -fname (usually set to 'regional')
    -exportDataFlag (whether the map should be exported or not)

  Retrieves desired data from mySQL database
  Feeds data into structuredMap() to reformat
  Feeds reformatted data into bokehMap() for graphing/mapping 

### structuredMap()
  Takes in:
    -DateFrame (consisting of longs, lats, variable   being measured, and times)
    -Table name
    -Variable name

  Creates lists of unique latitudes, longitudes, and time values
  Creates list of variable values and reshapes to mirror long/lat values

  Returns:
      -reshaped variable, long, lat arrays
      -subject of intended map: "variable + unit + time"
      -variable and table name

### bokehMap()
  Takes in:
    -data (variable values), lat, long arrays
    -subject string ("variable + unit + time")
    -fname (always seems to be set to regional)
    -table and variable lists

  Constructs and displays the map

### getUnit()
  Takes in:
    -table and variable names
  Returns:
    -the variable's unit of measurement
