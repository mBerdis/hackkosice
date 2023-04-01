import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Line, Ellipse
from kivy.properties import ObjectProperty

from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App
from kivy.lang import Builder

kv = '''
FloatLayout:
    MyMapView:
        m1: marker1
        m2: marker2
        size_hint: 1, 0.9
        pos_hint: {'y':0.1}
        zoom: 15
        lat: 48.7145
        lon: 21.2503
        double_tap_zoom: True
        MapMarker:
            id: marker1
            lat: 48.7144
            lon: 21.2506
            on_release: app.marker_released(self)
        MapMarker:
            id: marker2
            lat:  48.7154
            lon: 21.2506
            on_release: app.marker_released(self)
            
    Button:
        size_hint: 0.1, 0.1
        text: 'info'
        on_release: app.info()
'''

class MyMapView(MapView):
    grp = ObjectProperty(None)

    def do_update(self, dt):  # this over-rides the do_update() method of MapView
        super(MyMapView, self).do_update(dt)
        self.draw_lines()

    # draw the lines
    def draw_lines(self):
        # Define the radius of the Earth in kilometers
        R = 6371.01

        # Define the center point as a list of latitude and longitude coordinates in degrees
        center_point = [self.m1.lat, self.m1.lon]

        # Convert the latitude and longitude coordinates to radians
        lat1 = math.radians(center_point[0])
        lon1 = math.radians(center_point[1])

        # Calculate the distance from the center point to a point 1 kilometer to the north, south, east, and west
        d = 1  # 1 kilometer
        lat_north = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(0))
        lon_north = lon1 + math.atan2(math.sin(0) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_north))

        lat_south = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(math.pi))
        lon_south = lon1 + math.atan2(math.sin(math.pi) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_south))

        lat_east = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(math.pi/2))
        lon_east = lon1 + math.atan2(math.sin(math.pi/2) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_east))

        lat_west = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(3*math.pi/2))
        lon_west = lon1 + math.atan2(math.sin(3*math.pi/2) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_west))

        # Convert the latitude and longitude coordinates back to degrees
        lat_north = math.degrees(lat_north)
        lon_north = math.degrees(lon_north)
        north = [lat_north, lon_north]

        lat_south = math.degrees(lat_south)
        lon_south = math.degrees(lon_south)
        south = [lat_south, lon_south]

        lat_east = math.degrees(lat_east)
        lon_east = math.degrees(lon_east)
        east = [lat_east, lon_east]

        lat_west = math.degrees(lat_west)
        lon_west = math.degrees(lon_west)
        west = [lat_west, lon_west]

        points = [north, south, east, west]  # get the points for the lines from somewhere

        radius = ((lat_north - self.m1.lat) ** 2 + (lon_north - self.m1.lon) ** 2) ** 0.5

        #scale = float(1 * self.zoom)
        #print(scale)
        print(radius)
        circles = Ellipse(pos = [self.m1.center_x - radius, self.m1.y - radius], size= [radius, radius])

        self.mapview.meters_to_pixels()
        radius_pixels = self.parent.mapview.meters_to_pixels(radius, self.parent.mapview.zoom)

        lines = Line(ellipse=(north, south, east, west))
        #lines.points = points
        lines.width = 2
        if self.grp is not None:
            # just update the group with updated lines lines
            self.grp.clear()
            self.grp.add(lines)
            self.grp.add(circles)
        else:
            with self.canvas.after:
                #  create the group and add the lines
                Color(1,0,0,1)  # line color
                self.grp = InstructionGroup()
                self.grp.add(lines)
                self.grp.add(circles)


class MapViewApp(App):
    def build(self):
        return Builder.load_string(kv)

    def info(self, *args):
        print(self.root.ids.marker1)
        print(self.root.ids.marker2)

    def marker_released(self, marker):
        print(marker)

MapViewApp().run()