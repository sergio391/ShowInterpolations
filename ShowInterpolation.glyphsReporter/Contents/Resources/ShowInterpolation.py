#!/usr/bin/env python
# encoding: utf-8

import objc
from Foundation import *
from AppKit import *
import sys, os, re

MainBundle = NSBundle.mainBundle()
path = MainBundle.bundlePath() + "/Contents/Scripts"
if not path in sys.path:
	sys.path.append( path )

import GlyphsApp

ServiceProvider = NSClassFromString("GSServiceProvider").alloc().init()
GlyphsReporterProtocol = objc.protocolNamed( "GlyphsReporter" )

class ShowInterpolation ( NSObject, GlyphsReporterProtocol ):
	
	def init( self ):
		"""
		Put any initializations you want to make here.
		"""
		try:
			#Bundle = NSBundle.bundleForClass_( NSClassFromString( self.className() ));
			
			
			return self
		except Exception as e:
			self.logToConsole( "init: %s" % str(e) )
	
	def interfaceVersion( self ):
		"""
		Distinguishes the API version the plugin was built for. 
		Return 1.
		"""
		try:
			return 1
		except Exception as e:
			self.logToConsole( "interfaceVersion: %s" % str(e) )
	
	def title( self ):
		"""
		This is the name as it appears in the menu in combination with 'Show'.
		E.g. 'return "Nodes"' will make the menu item read "Show Nodes".
		"""
		try:
			return "Interpolations"
		except Exception as e:
			self.logToConsole( "title: %s" % str(e) )
	
	def keyEquivalent( self ):
		"""
		The key for the keyboard shortcut. Set modifier keys in modifierMask() further below.
		Pretty tricky to find a shortcut that is not taken yet, so be careful.
		If you are not sure, use 'return None'. Users can set their own shortcuts in System Prefs.
		"""
		try:
			return None
		except Exception as e:
			self.logToConsole( "keyEquivalent: %s" % str(e) )
	
	def modifierMask( self ):
		"""
		Use any combination of these to determine the modifier keys for your default shortcut:
			return NSShiftKeyMask | NSControlKeyMask | NSCommandKeyMask | NSAlternateKeyMask
		Or:
			return 0
		... if you do not want to set a shortcut.
		"""
		try:
			return 0
		except Exception as e:
			self.logToConsole( "modifierMask: %s" % str(e) )
	
	def glyphInterpolation( self, thisGlyph, thisInstance ):
		"""
		Yields a layer.
		"""
		try:
			try:
				# Glyphs 1.x syntax:
				thisInterpolation = thisInstance.instanceInterpolations()
			except:
				# Glyphs 2.x syntax:
				thisInterpolation = thisInstance.instanceInterpolations
			interpolatedLayer = thisGlyph.decomposedInterpolate_( thisInterpolation )
			interpolatedLayer.roundCoordinates()
			if len( interpolatedLayer.paths ) != 0:
				return interpolatedLayer
			else:
				return None
		except Exception as e:
			self.logToConsole( "glyphInterpolation: %s" % str(e) )
			return None
	
	def colorForParameterValue( self, parameterString ):
		"""
		Turns '0.3;0.4;0.9' into RGB values and returns an NSColor object.
		"""
		try:
			# default color:
			RGBA = [ 0.4, 0.0, 0.3, 0.15 ]
			
			# if set, take user input as color:
			if parameterString is not None:
				parameterValues = parameterString.split(";")
				for i in range(len( parameterValues )):
					thisValueString = parameterValues[i]
					try:
						thisValue = abs(float( thisValueString ))
						if thisValue > 1.0:
							thisValue %= 1.0
						RGBA[i] = thisValue
					except Exception as e:
						pass
						# self.logToConsole( "Could not convert '%s' (from '%s') to a float. Keeping default." % (thisValueString, parameterString) )
			
			# return the color:
			thisColor = NSColor.colorWithCalibratedRed_green_blue_alpha_( RGBA[0], RGBA[1], RGBA[2], RGBA[3] )
			return thisColor
		except Exception as e:
			self.logToConsole( "colorForParameterValue: %s" % str(e) )
	
	def drawForegroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed IN FRONT OF the paths.
		Setting a color:
			NSColor.colorWithCalibratedRed_green_blue_alpha_( 1.0, 1.0, 1.0, 1.0 ).set() # sets RGBA values between 0.0 and 1.0
			NSColor.redColor().set() # predefined colors: blackColor, blueColor, brownColor, clearColor, cyanColor, darkGrayColor, grayColor, greenColor, lightGrayColor, magentaColor, orangeColor, purpleColor, redColor, whiteColor, yellowColor
		Drawing a path:
			myPath = NSBezierPath.alloc().init()  # initialize a path object myPath
			myPath.appendBezierPath_( subpath )   # add subpath to myPath
			myPath.fill()   # fill myPath with the current NSColor
			myPath.stroke() # stroke myPath with the current NSColor
		To get an NSBezierPath from a GSPath, use the bezierPath() method:
			myPath.bezierPath().fill()
		You can apply that to a full layer at once:
			if len( myLayer.paths > 0 ):
				myLayer.bezierPath()       # all closed paths
				myLayer.openBezierPath()   # all open paths
		See:
		https://developer.apple.com/library/mac/documentation/Cocoa/Reference/ApplicationKit/Classes/NSBezierPath_Class/Reference/Reference.html
		https://developer.apple.com/library/mac/documentation/cocoa/reference/applicationkit/classes/NSColor_Class/Reference/Reference.html
		"""
		try:
			pass
		except Exception as e:
			self.logToConsole( str(e) )
	
	def drawBackgroundForLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed BEHIND the paths.
		"""
		try:
			if False: #change to False if you want to activate
				pass
			else:
				Glyph = Layer.parent
				Font = Glyph.parent
				Instances = [ i for i in Font.instances if i.active ]
			
				if len( Instances ) > 0:
					# display all instances that have a custom parameter:
					displayedInterpolationCount = 0
					for thisInstance in Instances:
						showInterpolationValue = thisInstance.customParameters["ShowInterpolation"]
						if showInterpolationValue is not None:
							interpolatedLayer = self.glyphInterpolation( Glyph, thisInstance )
							displayedInterpolationCount += 1
							if interpolatedLayer is not None:
								self.colorForParameterValue( showInterpolationValue ).set()
								interpolatedLayer.bezierPath().fill()
					
					# if no custom parameter is set, display them all:
					if displayedInterpolationCount == 0:
						self.colorForParameterValue( None ).set()
						for thisInstance in Instances:
							interpolatedLayer = self.glyphInterpolation( Glyph, thisInstance )
							if interpolatedLayer is not None:
								interpolatedLayer.bezierPath().fill()
		except Exception as e:
			self.logToConsole( "drawBackgroundForLayer_: %s" % str(e) )
	
	def drawBackgroundForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed behind the paths, but for inactive masters.
		"""
		try:
			if True: #change to False if you want to activate
				pass
			else:
				Glyph = Layer.parent
				Font = Glyph.parent
				Instances = [ i for i in Font.instances if i.active ]
			
				if len( Instances ) > 0:
					displayedInterpolationCount = 0
					for thisInstance in Instances:
						showInterpolationValue = thisInstance.customParameters["ShowInterpolation"]
						interpolatedLayer = self.glyphInterpolation( Glyph, thisInstance )
						if showInterpolationValue is not None:
							displayedInterpolationCount += 1
							if interpolatedLayer is not None:
								self.colorForParameterValue( showInterpolationValue ).set()
								interpolatedLayer.roundCoordinates()
								interpolatedLayer.bezierPath().fill()
					if displayedInterpolationCount == 0:
						self.colorForParameterValue( None ).set()
						for thisInstance in Instances:
							interpolatedLayer = self.glyphInterpolation( Glyph, thisInstance )
							interpolatedLayer.roundCoordinates()
							if interpolatedLayer is not None:
								interpolatedLayer.bezierPath().fill()
		except Exception as e:
			self.logToConsole( str(e) )
	
	def needsExtraMainOutlineDrawingForInactiveLayer_( self, Layer ):
		"""
		Whatever you draw here will be displayed in the Preview at the bottom.
		Remove the method or return True if you want to leave the Preview untouched.
		Return True to leave the Preview as it is and draw on top of it.
		Return False to disable the Preview and draw your own.
		In that case, don't forget to add Bezier methods like in drawForegroundForLayer_(),
		otherwise users will get an empty Preview.
		"""
		return True
	
	def getDisplayString( self ):
		listOfGlyphNames = []
		myTextPieces = self.controller.activeEditViewController().graphicView().displayString().replace("\n"," ").split(" ")
		
		for thisPiece in myTextPieces:
			if thisPiece.startswith("/"):
				for thisName in thisPiece.split("/"):
					listOfGlyphNames.append(thisName)
			elif thisPiece == "":
				if listOfGlyphNames[-1] != "space":
					listOfGlyphNames.append("space")
			else:
				for thisLetter in thisPiece:
					glyphName = ServiceProvider.nameStringFromUnicodeString_(thisLetter)[1:]
					listOfGlyphNames.append( glyphName )
					
	def getScale( self ):
		"""
		self.getScale() returns the current scale factor of the Edit View UI.
		Divide any scalable size by this value in order to keep the same apparent pixel size.
		"""
		try:
			return self.controller.graphicView().scale()
		except:
			self.logToConsole( "Scale defaulting to 1.0" )
			return 1.0
	
	def setController_( self, Controller ):
		"""
		Use self.controller as object for the current view controller.
		"""
		try:
			self.controller = Controller
		except Exception as e:
			self.logToConsole( "Could not set controller" )
	
	def logToConsole( self, message ):
		"""
		The variable 'message' will be passed to Console.app.
		Use self.logToConsole( "bla bla" ) for debugging.
		"""
		myLog = "Show %s plugin:\n%s" % ( self.title(), message )
		print myLog
		NSLog( myLog )
