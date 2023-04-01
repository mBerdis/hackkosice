# Code to create different polygons using Ellipse

# import kivy module
import kivy

# this restrict the kivy version i.e
# below this kivy version you cannot
# use the app or software
kivy.require("1.9.1")

# base Class of your App inherits from the App class.
# app:always refers to the instance of your application
from kivy.app import App

# The GridLayout arranges children in a matrix.
# It takes the available space and
# divides it into columns and rows,
# then adds widgets to the resulting “cells”.
from kivy.uix.gridlayout import GridLayout

# creating the Layout class
class Ellipsekv(GridLayout):
	pass

# creating the App class
class EllipseApp(App):
	def build(self):
		return Ellipsekv()

# run the App
if __name__=='__main__':
	EllipseApp().run()
