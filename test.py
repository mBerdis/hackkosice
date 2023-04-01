from kivy.app import App
from kivy_garden.mapview import MapView

class MyMapView(MapView):
    def on_touch_down(self, touch):
        if touch.is_double_tap:
            radius_meters = 5000 # Set the radius to 5 kilometers
            radius_pixels = self.meters_to_pixels(radius_meters, self.zoom)
            print(f"Radius in pixels: {radius_pixels}")

        return super().on_touch_down(touch)

class MyApp(App):
    def build(self):
        return MyMapView()

MyApp().run()
