import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import ObjectProperty

from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App
from kivy.lang import Builder

kv = '''
FloatLayout:
    MyMapView:
        m1: marker1
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
        d = 2  # 2x1 kilometer
        lat_north = math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(0))
        lon_north = lon1 + math.atan2(math.sin(0) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_north))
        lat_north = math.degrees(lat_north)
        lon_north = math.degrees(lon_north)

        marker = MapMarker(lat = lat_north, lon = lon_north)
        self.add_marker(marker)
        radius = marker.y - self.m1.y
        self.remove_marker(marker)

        lines = Ellipse(pos = (self.m1.center_x - radius/2, self.m1.center_y - radius/2), size = (radius, radius))

        if self.grp is not None:
            # just update the group with updated lines lines
            self.grp.clear()
            self.grp.add(lines)
        else:
            with self.canvas.after:
                #  create the group and add the lines
                Color(1,0,0,0.4)  # line color
                self.grp = InstructionGroup()
                self.grp.add(lines)


class MapViewApp(App):
    def build(self):
        return Builder.load_string(kv)

    def info(self, *args):
        print(self.root.ids.marker1)
        print(self.root.ids.marker2)

    def marker_released(self, marker):
        print(marker)

MapViewApp().run()