#Author-Sam DeRose
#Description-Auto-generates a greenhouse design based on your specific environment and needs. 

import adsk.core, adsk.fusion
import urllib.request
from html.parser import HTMLParser

############### PULL INPUTS FROM WEB

response = urllib.request.urlopen('http://samderose.netau.net/test_page1.html')
pageContentsBytes = response.read()
pageContents = pageContentsBytes.decode("utf-8") # convert byte object to string

print(pageContents)

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)
    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)
    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser(strict=False)
parser.feed(pageContents)

# add text parsing here


############### VARIABLE DEFINITIONS

# units in feet
wallHeight = 6
roofHeight = 9
width = 10
length = 10
insulation = 10 # cm!!!!


# convert ft to cm
wallHeight = wallHeight * 30.48
roofHeight = roofHeight * 30.48
width = width * 30.48
length = length * 30.48


############### SETUP

app = adsk.core.Application.get()
ui = app.userInterface

# this line makes a new document file, uncomment to allow script to run in current file
#doc = app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
design = app.activeProduct

# Get the root component of the active design.
rootComp = design.rootComponent


############### SKETCH 1

# Create a new sketch on the xy plane.
sketches = rootComp.sketches;
xyPlane1 = rootComp.xYConstructionPlane
sketch1 = sketches.add(xyPlane1)

# Draw two connected lines.
lines = sketch1.sketchCurves.sketchLines;
line1 = lines.addByTwoPoints(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(width, 0, 0))
line2 = lines.addByTwoPoints(line1.endSketchPoint, adsk.core.Point3D.create(width, wallHeight, 0))
line3 = lines.addByTwoPoints(line2.endSketchPoint, adsk.core.Point3D.create(width/2, roofHeight, 0))
line4 = lines.addByTwoPoints(line3.endSketchPoint, adsk.core.Point3D.create(0, wallHeight, 0))
line5 = lines.addByTwoPoints(line4.endSketchPoint, adsk.core.Point3D.create(0, 0, 0))



############### EXTRUDE SKETCH 1


# Get the profile defined by the circle
prof1 = sketch1.profiles.item(0)

# Create an extrusion input
extrudes1 = rootComp.features.extrudeFeatures
extInput = extrudes1.createInput(prof1, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) # extInput defines the parameters for the extrude

# Define that the extent is a distance extent of LENGTH
distance = adsk.core.ValueInput.createByReal(length)
# Set the distance extent to be one-sided
extInput.setDistanceExtent(False, distance)
# Set the extrude to be a solid one
extInput.isSolid = True

# Create the extrusion
ext1 = extrudes1.add(extInput) # ext is the extruded feature




############### SHELL EXTRUSION 1

entities1 = adsk.core.ObjectCollection.create()
entities1.add(ext1.endFaces.item(0)) 
 
features = rootComp.features
shellFeats = features.shellFeatures
isTangentChain = False
shellFeatureInput = shellFeats.createInput(entities1, isTangentChain)
thickness = adsk.core.ValueInput.createByReal(insulation)
shellFeatureInput.insideThickness = thickness
shellFeats.add(shellFeatureInput)


############### SKETCH 2 - MAKE THE END CAP

# Creat another sketch, and extrude it to cap the end
xyPlane2 = rootComp.xYConstructionPlane
sketch2 = sketches.add(xyPlane2)

# Draw the sketch for the greenhouse outline
lines2 = sketch2.sketchCurves.sketchLines;
line2_1 = lines2.addByTwoPoints(adsk.core.Point3D.create(0, 0, length), adsk.core.Point3D.create(width, 0, length))
line2_2 = lines2.addByTwoPoints(line2_1.endSketchPoint, adsk.core.Point3D.create(width, wallHeight, length))
line2_3 = lines2.addByTwoPoints(line2_2.endSketchPoint, adsk.core.Point3D.create(width/2, roofHeight, length))
line2_4 = lines2.addByTwoPoints(line2_3.endSketchPoint, adsk.core.Point3D.create(0, wallHeight, length))
line2_5 = lines2.addByTwoPoints(line2_4.endSketchPoint, adsk.core.Point3D.create(0, 0, length))




############### EXTRUDE SKETCH 2

# Get the profile defined by the sketch
prof2 = sketch2.profiles.item(0)

# Create an extrusion input
extrudes2 = rootComp.features.extrudeFeatures
extInput2 = extrudes2.createInput(prof2, adsk.fusion.FeatureOperations.NewBodyFeatureOperation) # extInput defines the parameters for the extrude

# Define that the extent is a distance extent of INSOLATION
distance2 = adsk.core.ValueInput.createByReal(insulation)
# Set the distance extent to be one-sided
extInput2.setDistanceExtent(False, distance2)
# Set the extrude to be a solid one
extInput2.isSolid = True

# Create the extrusion
ext2 = extrudes2.add(extInput2) # ext is the extruded feature









#################### DEFAULT STARTER CODE ##########################

#def run(context):
#    ui = None
#    try:
#        app = adsk.core.Application.get()
#        ui  = app.userInterface
#        ui.messageBox('Hello script')
#
#    except:
#        if ui:
#            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
