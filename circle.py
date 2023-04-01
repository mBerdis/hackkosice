from kivy.app import App
from kivy_garden.mapview import MapView
from kivy.graphics import Canvas, Color, Ellipse, Line
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget

# class in which we are creating the canvas
class CanvasWidget(Widget):
     
    def __init__(self, **kwargs):
        super(CanvasWidget, self).__init__(**kwargs)
        
 
        # Arranging Canvas
        with self.canvas:
 
            Color(0.126, 0.11, 0.23, 0.5)  # set the colour
 
            x1 = 42
            y1 = 20

            x_center = 40
            y_center = 20

            # Setting the size and position of canvas
            self.rect = Line(bezier=(40, 20, 41, 21, 42, 20, 41,19))
            radius = ((x1 - x_center) ** 2 + (y1 - y_center) ** 2) ** 0.5

            print("here")
            print(radius)
            self.rect = Ellipse(pos=(x_center - radius, y_center - radius), size=(radius * 2, radius * 2))
 
            # Update the canvas as the screen size change
            #self.bind(pos = self.update_rect, size = self.update_rect)
 
    # update function which makes the canvas adjustable.
    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = self.size


class RootWidget(AnchorLayout):
    lat = NumericProperty(48.7145)
    lon = NumericProperty(21.2503)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.anchor_x = 'right'
        self.anchor_y = 'top'

        mapview = MapView(zoom=12, lat=self.lat, lon=self.lon)
        self.add_widget(mapview)

        print(mapview.zoom)

        canvas = CanvasWidget()
        mapview.add_widget(canvas)

    def centerOnUser(self):
        pass

class MapViewApp(App):
    def build(self):
        return RootWidget()
    
MapViewApp().run()