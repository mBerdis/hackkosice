from kivy.app import App
from kivy_garden.mapview import MapView
from kivy.graphics import Canvas, Color, Ellipse, Rectangle
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
 
            # Setting the size and position of canvas
            self.rect = Ellipse(pos = self.center, size=(50,500))
            self.rect = Ellipse(pos = (0,400), size=(500,500))
            self.rect = Ellipse(pos = (500,54), size=(50,520))
 
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

        mapview = MapView(zoom=11, lat=self.lat, lon=self.lon)
        self.add_widget(mapview)

        canvas = CanvasWidget()
        mapview.add_widget(canvas)

        touchBarbtn1 = Button(text='Unlock', size_hint=(0.1, 0.1))
        touchBarbtn1.bind(on_press=lambda x: self.centerOnUser())
        self.add_widget(touchBarbtn1)

    def centerOnUser(self):
        pass

class MapViewApp(App):
    def build(self):
        return RootWidget()
    
MapViewApp().run()