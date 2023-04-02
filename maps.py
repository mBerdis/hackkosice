import csv
import sys
import math

from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup, Canvas
from kivy.graphics.vertex_instructions import Ellipse
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox

from kivy_garden.mapview import MapView, MapMarker, MapMarkerPopup
from kivy.app import App
from kivy.lang import Builder

class SchoolMarker(MapMarkerPopup):
    color = (0, 0, 1, 0.5)

class Markers(MapMarker):

    def __init__(self, filename, lat_index, lon_index, type_filter, label):

        def loadMarkers():
            with open(filename, newline='', encoding='utf-8') as csvfile:
                csvreader = csv.reader(csvfile)
                headers = next(csvreader)
                data = list(csvreader)

            markers = list()

            for marker in data:
                if filename == "POIs.csv":
                    if marker[2] == type_filter:
                        map_marker = MapMarkerPopup(lat=marker[lat_index], lon=marker[lon_index], popup_size=(100, 50))
                        map_marker.add_widget(Label(text= label + ": " + marker[2], color=(1,0,1,1)))
                    else:
                        continue
                else:
                    map_marker = MapMarkerPopup(lat=marker[lat_index], lon=marker[lon_index], popup_size=(100, 50))
                    map_marker.add_widget(Label(text= label + ": " + marker[2], color=(1,0,1,1)))
                
                # Define the radius of the Earth in kilometers
                R = 6371.01

                # Convert the latitude and longitude coordinates to radians
                lat1 = math.radians(map_marker.lat)
                lon1 = math.radians(map_marker.lon)

                # Calculate the distance from the center point to a point 1 kilometer to the north, south, east, and west
                d = 2  # 2x0.5 kilometer
                lat_north = math.degrees(math.asin(math.sin(lat1) * math.cos(d/R) + math.cos(lat1) * math.sin(d/R) * math.cos(0)))
                lon_north = math.degrees(lon1 + math.atan2(math.sin(0) * math.sin(d/R) * math.cos(lat1), math.cos(d/R) - math.sin(lat1) * math.sin(lat_north)))

                north_point = [lat_north, lon_north]
                markers.append([map_marker, north_point])

            return markers

        super().__init__()
        self.Markers = loadMarkers()

class Mapp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        mapview = MapView(zoom=11, lat=48.7145, lon=21.2503)

        max_zoom = 20
        min_zoom = 11

        show_schools = None

        def on_zoom(mapview, zoom):
            if zoom > max_zoom:
                mapview.zoom = max_zoom
            elif zoom < min_zoom:
                mapview.zoom = min_zoom
           
        mapview.bind(zoom=on_zoom)

        markers = Markers("stredne_skoly.csv", 19, 20, "", "Skola")

        for marker in markers.Markers:
            mapview.add_marker(marker[0])

        def update(mapview, zoom):
            if show_schools is False:
                pass

            for child in mapview.canvas.children:
                if type(child) is Ellipse:
                    mapview.canvas.remove(child)

            for marker in markers.Markers:
                tmp_marker = MapMarker(lat = marker[1][0], lon = marker[1][1])
                mapview.add_marker(tmp_marker)
                radius = tmp_marker.y - marker[0].y
                mapview.remove_marker(tmp_marker)

                with mapview.canvas:
                    Color(0,1,0,0.08)  # line color
                    circle = Ellipse(pos = (marker[0].center_x - radius/2, marker[0].center_y - radius/2), size = (radius, radius))
                    west, south, east, north=mapview.get_bbox()
                    west, south = mapview.get_window_xy_from(west, south, mapview.zoom)
                    east, north = mapview.get_window_xy_from(east, north, mapview.zoom)
                    
                    if (west < marker[0].center_x - radius/2 and marker[0].center_x- radius/2 < east and south < marker[0].center_y- radius/2 and  marker[0].center_y- radius/2 < north and west < marker[0].center_x + radius/2 and marker[0].center_x+ radius/2 < east and south < marker[0].center_y+ radius/2 and  marker[0].center_y+ radius/2 < north):
                        mapview.canvas.add(circle)
                        #print(str(west) +" < "+ str(marker[0].center_x + radius/2) +" and "+ str(marker[0].center_x- radius/2) +" < "+ str(east) +" and "+ str(south) +" < "+ str(marker[0].center_y- radius/2) +" and "+  str(marker[0].center_y+ radius/2) +" < "+ str(north))                
                    else:
                        mapview.canvas.remove(circle)


        mapview.bind(lon=update)
        visible_markers = True

        cbox_skoly = CheckBox(active=True)
        labels = Label(text="Stredne skoly")

        def on_checkbox_skoly_active(checkbox, value):
            if value is False:
                self.show_schools = False
                for marker in markers.Markers:
                    mapview.remove_marker(marker[0])
                for child in mapview.canvas.children:
                    if type(child) is Ellipse:
                        mapview.canvas.remove(child)
            else:
                show_schools = True
                for marker in markers.Markers:
                    mapview.add_marker(marker[0])

        cbox_skoly.bind(active=on_checkbox_skoly_active)

        # BANKY

        cbox_banky = CheckBox(active=False)
        labelBank = Label(text="Banky")

        def on_checkbox_banky_active(checkbox, value):
            if value is False:
                self.mapview = MapView(zoom=11, lat=48.7145, lon=21.2503)
            else:
                markers = Markers("POIs.csv", 4, 5, "Všeobecná ambulancia pre deti a dorast", "Všeob. ambulancia")
                for marker in markers.Markers:
                    mapview.add_marker(marker[0])

        cbox_banky.bind(active=on_checkbox_banky_active)

        ###

        file_path = "zastavky_mhd.csv"
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            headers = next(csvreader)
            dota = list(csvreader)

        mhd_markers = list()
        mhdlst = list()

        for marker in dota:
            if marker[7] not in mhdlst:
                map_marker = SchoolMarker(lat=marker[10], lon=marker[9], popup_size=(100, 50))
                map_marker.add_widget(Label(text="Zastavka: "+marker[7], color=(1, 0, 1, 1)))
                mhd_markers.append(map_marker)
                mhdlst.append(marker[7])
                mapview.add_marker(map_marker)

        cbox_mhd = CheckBox(active=True)
        labelm = Label(text="zastavky MHD")

        def on_checkbox_mhd_active(checkbox, value):
            if value is False:
                for marker in mhd_markers:
                    mapview.remove_marker(marker)
            else:
                for marker in mhd_markers:
                    mapview.add_marker(marker)

        cbox_mhd.bind(active=on_checkbox_mhd_active)

        box = BoxLayout(pos=(300, 350), size_hint=(.25, .18))

        box.add_widget(cbox_mhd)
        box.add_widget(labelm)
        box.add_widget(cbox_skoly)
        box.add_widget(labels)
        box.add_widget(cbox_banky)
        box.add_widget(labelBank)
        layout.add_widget(box)
        layout.add_widget(mapview)

        return layout


Mapp().run()