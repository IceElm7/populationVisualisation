# Visualising GBplaces.csv using matplotlib module of Python
# Joseph Amoss - 5th Assignment: Intro to Programming
# Year 2 Physics

# Plots the towns/ cities of Great Britian by Longitude v. Latitude
# Colour and size of scatter marker give a representation of population size
# Includes functionality to click on place and see extra information
# Cannot view information on Westminster as it has the same co-ords as London
#--------------------------------------------------------------------------------

import matplotlib.pyplot as plt;
import matplotlib.cm as cm
import pandas as pd
# imported as code was written in alternative IDE
# this allows the same functionality in spyder 2.3.8
#from IPython import get_ipython
#get_ipython().run_line_magic('matplotlib', 'qt')

# tests if the correct file is in the directory to be read in
try:
    readFile = open('GBplaces.csv','r')
    openFile = 1;
    # sets variable so that if file can be opened, the code can progress
except:
    print("An error occurred whilst opening the file")
    # gives elegant error message if the file is missing
    openFile = 0

readFile = open('GBplaces.csv','r');

# initial list to run all the input data into
placeInfo = []
# set up multiple arrays so each set of information can be called separately
name = []
type = []
population = []
latitude = []
longitude = []

# ensures that the first line is missed as this is merely a title row
skipTheLine = 0

# once file is successfully opened, runs through each line in GBplaces
if openFile:
    for line in readFile:
        # splits up input file from list of lists into placeInfo array
        if skipTheLine:
            # makes array with each element being a line in GBplaces
            splitEachCity = line.split('\n');
            # makes list of list with each element in inner list being a piece of information about one place
            splitEachCity = splitEachCity[0].split(',')
            # places all this information into a single array
            placeInfo.append(splitEachCity);

        skipTheLine = 1

# closes GBplaces file
readFile.close()
# changes output figure to a nice, easily readable size
fig = plt.figure(figsize=(10,10))

# splits up placeInfo and places each set of information into its own array
# this allows for all information to be used independently of one another
for i in range(len(placeInfo)):
    name.append(placeInfo[i][0]);
    type.append(placeInfo[i][1]);
    # set population as integer so it displays without a decimal point
    population.append(int(placeInfo[i][2]));
    # converted latitude and longitude to float numbers as these are being plotted
    latitude.append(float(placeInfo[i][3]));
    longitude.append(float(placeInfo[i][4]));



# fixes population size so the scatter points are discernible on a graph

scaledPopulation = [(0.0001*population[i]) for i in range(len(population))]

# hard codes in colour exception for London
# as Londons population is much larger than all the others, the colour map doesn't give a great visualisation of this
# the scaled population is set to 130 so it is still darker than other places, but a colour gradient is more obvious
# 22 Feb 2021 - Not sure why I included this; originally wasn't even implemented as was aboce scaledPopulation = ...
# left for prosperity
'''
for i in range(len(name)):
    if name[i].lower() == "london":
        scaledPopulation[i] = 130
'''



# changes colour heat scale to red -> yellow -> green (looked the nicest)
cm = cm.get_cmap("RdYlGn")

# defined scatter plot so that colour scale could be linked to the points
# sets x & y to longitude and latitude
# points are circles whose colour and size represent the population
# picker defines the region the onpick event can operate
# vmin & vmax set the min/ max values for the colour scale (and alpha is the transparency)
scatter = plt.scatter(longitude,latitude, c=scaledPopulation, s=scaledPopulation,
                      picker=4, vmin=8, vmax=130, cmap=cm, alpha=0.5)

# sets reasonable limits for the axes based on the data
plt.xlim(-5.0,2)
plt.ylim(49.5,58.0)

# writes the title and axis titles in readable font style
plt.xlabel("Longitude / Degrees", style ='italic')
plt.ylabel("Latitude / Degrees", style ='italic')
plt.title("GB Places represented by Longitude v. Latitude", fontweight='bold')

# inserts colour bar to the side for reference
cbar = plt.colorbar(scatter)
cbar.ax.set_ylabel("Relative Population Size")

# displays the data for each point upon clicking
# creates initial empty array for annotation
annotation = []

# defines what happens when a point is clicked on the figure
def onpick(event):
    # upon clicking a point, gives an index based on the position of the point in GBplaces
    ind = event.ind

    # removes any previous annotation on the figure
    annotation[0].remove()

    # resets annotation to give information based on the first index that appears
    # essentially if many points overlap, returns the first one it finds
    annotation[0] = plt.annotate("%s\nType: %s\nPopulation: %s" %(name[ind[0]], type[ind[0]], population[ind[0]]),
                                 xy=(longitude[ind[0]], latitude[ind[0]]), xytext=(-0.8, 57.1),
                                 arrowprops=dict(arrowstyle="-|>", connectionstyle="arc"))

    # draws this annotation 'over' the figure
    fig.canvas.draw()

# initial annotation that shows before clicking, informs user of functionality
annotation =[plt.annotate("Click on the points \nto find out more!", xy=(-0.8,57.3))]

# sets up the annotation array to run
annotation[0]

# required for onpick event to work
# maps the annotation onto figure
fig.canvas.mpl_connect('pick_event', onpick)

# displays the figure
plt.show()



