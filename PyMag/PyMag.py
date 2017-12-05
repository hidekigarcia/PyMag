from geomag import WorldMagneticModel
import math
from datetime import date
 
# Globals #
ROE = 6378.1 # Radius of Earth in Kilometers
EAST = math.radians(98.75389)
WEST = math.radians(279.0128)
NORTH = math.radians(8.89667)
SOUTH = math.radians(188.94)
NORTH_WEST = math.radians(323.9533)
 
 
class Point_Content:
    latitude=0
    longitude=0
    latitude_degrees=0
    longitude_degrees=0
    magnetic_field = 0
 
    def __init__(self,lat,lon):
        self.latitude=lat
        self.longitude=lon
 
    def __str__(self):
        return str(self.latitude_degrees) + "," + str(self.longitude_degrees) + "\n"
 
    def __repr__(self):
        return str(self)
 
def onepoint(lat1, lon1, brng1, d):
    lat2 = math.asin(math.sin(lat1)*math.cos(d / ROE) + math.cos(lat1)*math.sin(d / ROE)*math.cos(brng1)) #in radians
    lon2 = lon1 + math.atan2(math.sin(brng1)*math.sin(d / ROE)*math.cos(lat1), math.cos(d / ROE) - math.sin(lat1)*math.sin(lat2))
    lon2 = math.fmod((lon2 + 540), 360) - 180
    latD1 = (lat2) * 180 / math.pi
    lonD1 = (lon2) * 180 / math.pi
    p=Point_Content(lat2,lon2)
    p.latitude_degrees=latD1
    p.longitude_degrees = lonD1
    return p
 
def points(lat1, lon1, brng1, d, WMM):
    lat2=0
    lon2=0
    latD1=0
    lonD1=0
    p = []
    p.append(Point_Content(lat1, lon1))
    # Get the data for the first point passed
    p[0].latitude_degrees = math.degrees(lat1)
    p[0].longitude_degrees = math.degrees(lon1)
    p[0].magnetic_field=WMM.calc_mag_field(p[0].latitude_degrees,p[0].longitude_degrees, 29, unit='m' ).total_intensity
 
    # Calculate the rest of the points
    for i in range(1,11):
       
        lat2 = math.asin(math.sin(lat1)*math.cos(d / ROE) + math.cos(lat1)*math.sin(d / ROE)*math.cos(brng1)) #in radians
        lon2 = lon1 + math.atan2(math.sin(brng1)*math.sin(d / ROE)*math.cos(lat1), math.cos(d / ROE) - math.sin(lat1)*math.sin(lat2))
        lon2 = math.fmod((lon2 + 540), 360) - 180 #in radians
 
        p.append(Point_Content(lat2,lon2))
 
        latD1 = (lat2) * 180 / math.pi
        lonD1 = (lon2) * 180 / math.pi
        p[i].latitude_degrees = latD1
        p[i].longitude_degrees = lonD1
        p[i].magnetic_field=WMM.calc_mag_field(p[i].latitude_degrees,p[i].longitude_degrees, 29, unit='m' ).total_intensity
        d = d + .010
    return p
 
def main():
    WMM = WorldMagneticModel("WMM.COF")
    latd = 26.299824
    lond = -98.180454
    alt = 29 # m
    d=.01
 
    # Grab the first point NW of center
    FirstPoint = onepoint(math.radians(latd),math.radians(lond),NORTH_WEST,.35)
 
    Grid = [] # grid containing the points
    for i in range(0,11):
        Row = points(FirstPoint.latitude, FirstPoint.longitude,EAST,0.01, WMM)
        Grid.append(Row)
        FirstPoint = onepoint(FirstPoint.latitude, FirstPoint.longitude, SOUTH, 0.01)
 
    # Write contents of the grid to the file, latitude and longitude for plotting
    # TODO Make export to file an independent function out of main
    with open("data.txt", "w") as output:
        for i in range(0,len(Grid)):
            for j in range(0,len(Grid[i])):
                output.write(str(Grid[i][j].latitude_degrees) + "," + str(Grid[i][j].longitude_degrees) + " " +  "\n")
                print(str(Grid[i][j].latitude_degrees) + "," + str(Grid[i][j].longitude_degrees) + " " + "\n")
 
    PointsTogether = Grid[0] # the first array
    for i in range(1,len(Grid)):
        PointsTogether.extend(Grid[i]) # extend the existing array
 
    # TODO Sort the PointsTogether array
 
if __name__ == "__main__":
    main()