import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import ObjectProperty

from kivy_garden.mapview import MapView, MapMarker
from kivy.app import App
from kivy.lang import Builder

class MyMapView(MapView):
    grp = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        this = MapView(zoom=11, lat = 48.7145, lon = 21.2503)

    m1 = MapMarker(lat = 42, lon = 21)

    def do_update(self, ):  # this over-rides the do_update() method of MapView
        super(MyMapView, self).trigger_update
        self.draw_circle()

    # draw the circle
    def draw_circle(self):
        # Define the radius of the Earth in kilometers
        R = 6371.01

        # Convert the latitude and longitude coordinates to radians
        lat1 = math.radians(self.m1.lat)
        lon1 = math.radians(self.m1.lon)

        # Calculate the distance from the center point to a point 1 kilometer to the north, south, east, and west
        d = 2  # 2x1 kilometer
        lat_north = math.degrees(math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(0)))
        lon_north = math.degrees(lon1 + math.atan2(math.sin(0) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_north)))

        marker = MapMarker(lat = lat_north, lon = lon_north)
        self.add_marker(marker)
        radius = marker.y - self.m1.y
        self.remove_marker(marker)

        print(marker.x, marker.y)

        circle = Ellipse(pos = (self.m1.center_x - radius/2, self.m1.center_y - radius/2), size = (radius, radius))

        if self.grp is not None:
            # just update the group with updated circle circle
            self.grp.clear()
            self.grp.add(circle)
        else:
            with self.canvas.after:
                #  create the group and add the circle
                Color(1,0,0,0.4)  # line color
                self.grp = InstructionGroup()
                self.grp.add(circle)


class MapViewApp(App):
    def build(self):
        return MyMapView()

MapViewApp().run()