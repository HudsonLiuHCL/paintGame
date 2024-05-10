from cmu_graphics import *
import math,string,copy,random


# Object Orientation 
# *************************************************************************
# *************************************************************************

class selection:
    def __init__(self,shape,color):
        self.shape=shape
        self.color=color
    def __repr__(self):
        return f'{self.shape,self.color}'
        
class recLocation:
    def __init__(self,startX,startY,width,height):
        self.startX=startX
        self.startY=startY
        self.width=width
        self.height=height
    def __repr__(self):
        return f'{self.startX,self.startY,self.width,self.height}'
        
class circleLocation:
    def __init__(self,x,y,radius):
        self.x=x
        self.y=y
        self.radius=radius
        return f'{self.x,self.y,self.radius}'
    
    def __repr__(self):
        return f'{self.x,self.y,self.radius}'
        
class lineLocation:
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2
        return f'{self.x1,self.y1,self.x2,self.y2}'
    
    def __repr__(self):
        return f'{self.x1,self.y1,self.x2,self.y2}'
        
class polygonLocation:
    def __init__(self):
        self.points=[]
    
    def __repr__(self):
        return f'{self.points}'
        
    def addPoints(self,x,y):
        self.points.append(x)
        self.points.append(y)
        
class penLocation:
    def __init__(self):
        self.points=[]
    
    def __repr__(self):
        return f'{self.points}'
        
    def addPoints(self,x,y):
        self.points.append((x,y))
        
# Graphics
# *************************************************
# *************************************************
def onAppStart(app):
    app.stepsPerSecond=100
    app.colors=['red','orange','yellow','green','blue','purple','black','gray']
    app.polygon=[]
    app.colorSelectionLabel=[1,0,0,0,0,0,0,0]
    app.shapeSelectionLabel=[0,0,0,0,0]
    app.selectedColor='red'
    # draw shapes
    app.drawing=False
    app.selectedShape=None
    app.drawShapes=[]
    app.startingLocation=None
    # draw dragging  Line
    app.draggingLine=False
    app.drawDragShape=None
    # drawPolygon
    app.showPolygonDot=False
    app.polygonDot=[]
    app.polygonLocation=polygonLocation()
    app.penLocation=penLocation()
    app.mouseDragLocation=None
    # Z and Y feature
    app.removedList=[]
    app.wentBack=False   #check if a shape was drawn so that use cannot use Y feature

    
def redrawAll(app):
    drawBackground(app)
    drawPanel(app)
    drawPanelShapes(app)
    # drawshapes
    for v in app.drawShapes:
        selection,location=v
        drawBaseOnShape(app,selection,location)
    # draw dragging line
    if app.draggingLine==True and app.drawDragShape!=None:
        selection,location=app.drawDragShape
        drawDragLine(app,selection,location)
    # draw polygon dot
    if app.showPolygonDot==True:
        for i in range(len(app.polygonDot)):
            x,y=app.polygonDot[i]
            if i==0:
                drawLabel('x',x,y,fill='darkGreen')
            else:
                drawLabel('x',x,y,fill='red')
                
def drawPanelShapes(app):
    drawRect(10,65,20,20,fill='darkGray',border='dimGray')
    drawCircle(55,75,10,fill='dimGray',border='dimGray')
    drawLine(12,123,28,107,fill='dimGray')
    drawPolygon(45,110,62,105,59,125,49,120,fill='dimGray',border='dimGray')
    drawLabel(chr(0x270e),20,155,size=21,rotateAngle=100,font='symbols',fill='dimgray')
    drawLabel(chr(0x1f804),20,196,fill='dimgray',size=24,font='symbols')
    drawLabel(chr(0x1f806),55,196,fill='dimgray',size=24,font='symbols')
    
def drawBackground(app):
    drawRect(0,0,700,450,fill='gainsboro')
    drawRect(75,50,605,380,fill='white')
    drawLine(0,50,700,50)
    drawLine(75,50,75,450)
    drawLine(75,430,680,430)
    drawLine(680,50,680,430)
    drawLabel('112Paints',350,25,size=30,font='caveat')
    drawLabel('Fill Options',37,275,size=13)
    
def drawPanel(app):
    # draw color panel and green selection
    colorY=250
    for i in range(len(app.colors)):
        if app.colorSelectionLabel[i]==1:
            borderColor='green'
        else:
            borderColor='black'
        if i%2==0:
            colorY+=40
            drawRect(5,colorY,30,30,fill=app.colors[i],border=borderColor)
        else:
            drawRect(40,colorY,30,30,fill=app.colors[i],border=borderColor)
    ShapeY=20
    # draw tools panel and green selection
    for i in range(5):
        if app.shapeSelectionLabel[i]==1:
            borderColor='green'
        else:
            borderColor='black'
        if i%2==0:
            ShapeY+=40
            drawRect(5,ShapeY,30,30,fill=None,border=borderColor)
        else:
            drawRect(40,ShapeY,30,30,fill=None,border=borderColor)
    drawRect(5,180,30,30,fill=None,border='black')
    drawRect(40,180,30,30,fill=None,border='black')

def drawBaseOnShape(app,selection,location):
    color=selection.color
    if selection.shape=='rectangle':
        if location.width!=0 and location.height!=0:
            drawRect(location.startX,location.startY,location.width,location.height,fill=color)
    elif selection.shape=='circle':
        drawCircle(location.x,location.y,location.radius,fill=color)
    elif selection.shape=='line':
        drawLine(location.x1,location.y1,location.x2,location.y2,fill=color)
    elif selection.shape=='polygon':
        drawPolygon(*location.points,fill=color)
    elif selection.shape=='pen':
        for i in range(1,len(location.points)):
            previousX,previousY=location.points[i-1]
            x,y=location.points[i]
            drawLine(previousX,previousY,x,y,fill=color)
        
def drawDragLine(app,selection,location):
    color=selection.color
    if selection.shape=='rectangle':
        if location.width!=0 and location.height!=0:
            drawRect(location.startX,location.startY,location.width,location.height,fill=None,border=color)
    elif selection.shape=='circle':
        if location.radius!=0:
            drawCircle(location.x,location.y,location.radius,fill=None,border=color)
    elif selection.shape=='line':
        drawLine(location.x1,location.y1,location.x2,location.y2,fill=color)
    elif selection.shape=='pen':
        for i in range(1,len(location.points)):
            previousX,previousY=location.points[i-1]
            x,y=location.points[i]
            drawLine(previousX,previousY,x,y,fill=color)
        
def onMousePress(app,mouseX,mouseY):
    # z and y feature
    if mouseX>5 and mouseX<35 and mouseY>180 and mouseY<210:
        ctrilZ(app)
    if mouseX>40 and mouseX<70 and mouseY>180 and mouseY<210:
        ctrilY(app)
    # select tools
    if not inDrawBoard(app,mouseX,mouseY):
        selectColor(app,mouseX,mouseY)
        selectShape(app,mouseX,mouseY)
    else:
        app.draggingLine=True
        if app.selectedShape!='polygon':
            app.startingLocation=(mouseX,mouseY)
        else:
            # adding polygon to drawn shape if it is polygon
            select=selection(app.selectedShape,app.selectedColor)
            app.polygonLocation.addPoints(mouseX,mouseY)
            app.showPolygonDot=True
            app.polygonDot.append((mouseX,mouseY))
            initialX,initialY=app.polygonDot[0]
            if ((mouseX<initialX+5 and mouseX>initialX-5) or (mouseY<initialY+5 and mouseY>initialY-5)) and (len(app.polygonDot)>1):
                app.wentBack=False
                app.drawShapes.append([select,app.polygonLocation])
                app.showPolygonDot=False
                app.polygonDot=[]
                app.polygonLocation=polygonLocation()
    # cancel the dot on board if user selected other tools while drawing polygon
    if not inDrawBoard(app,mouseX,mouseY) and app.selectedShape!='polygon':
        # app.mouseDragLocation=None
        app.showPolygonDot=False
        app.polygonDot=[]
        app.polygonLocation=polygonLocation()
            
 
def onMouseDrag(app,mouseX,mouseY):
    if app.selectedShape!='polygon':
        # draw pen
        if inDrawBoard(app,mouseX,mouseY):
            app.drawing=True
            app.mouseDragLocation=mouseX,mouseY
            if app.selectedShape=='pen':
                select=selection(app.selectedShape,app.selectedColor)
                app.penLocation.addPoints(mouseX,mouseY)
                app.drawDragShape=(select,app.penLocation)
                app.wentBack=False
            else:
                startX,startY=app.startingLocation
                select,location=locationAndSelection(app,startX,startY,mouseX,mouseY)
                app.drawDragShape=select,location


def onMouseRelease(app,mouseX,mouseY):
    if app.drawing==True:
        if app.selectedShape=='pen':
            select=selection(app.selectedShape,app.selectedColor)
            app.drawShapes.append([select,app.penLocation])
            app.drawing=False
        if app.selectedShape!='polygon' and app.selectedShape!='pen':
            # draw circle,rectangle,and lines
            startX,startY=app.startingLocation
            location=None
            if inDrawBoard(app,mouseX,mouseY):
                x,y=mouseX,mouseY
            if not inDrawBoard(app,mouseX,mouseY):
                x,y=app.mouseDragLocation
            select,location=locationAndSelection(app,startX,startY,x,y)
            app.drawShapes.append([select,location])
            app.wentBack=False
            app.draggingLine=False
            app.drawing=False
    app.penLocation=penLocation()
            
def onKeyPress(app,key):
    if key=='z':
        ctrilZ(app)
    elif key=='y':
        ctrilY(app)

def ctrilZ(app):
    app.wentBack=True
    if len(app.drawShapes)!=0:
        app.removedList.append(app.drawShapes.pop())
        app.drawDragShape=None
        
def ctrilY(app):
    if app.wentBack==True:
        if len(app.removedList)!=0:
            app.drawShapes.append(app.removedList.pop())


def locationAndSelection(app,startX,startY,mouseX,mouseY):
    select=selection(app.selectedShape,app.selectedColor)
    location=None
    if app.selectedShape=='rectangle':
        width=abs(mouseX-startX)
        height=abs(mouseY-startY)
        # make sure rectangle can be drawn backward
        if mouseX-startX<0:
            startX-=width
        if mouseY-startY<0:
            startY-=height
        location=recLocation(startX,startY,width,height)
    if app.selectedShape=='circle':
        radius=circleRadius(startX,startY,mouseX,mouseY)
        # make sure the circle stays in the board
        if startX+radius>680:
            radius=680-startX
        if startX-radius<75:
            radius=startX-75
        if startY+radius>430:
            radius=430-startY
        if startY-radius<50:
            radius=startY-50
        location=circleLocation(startX,startY,radius)
    if app.selectedShape=='line':
        location=lineLocation(startX,startY,mouseX,mouseY)
    return select,location
    
def circleRadius(x1,y1,x2,y2):
    return ((x2-x1)**2+(y2-y1)**2)**0.5
    
def inDrawBoard(app,mouseX,mouseY):
    if mouseX>75 and mouseX<680 and mouseY>50 and mouseY<430:
        return True
    else:
        return False
        
def selectShape(app,x,y):
    if x>5 and x<35 and y>60 and y<90:
        app.selectedShape='rectangle'
        app.shapeSelectionLabel=[1,0,0,0,0]
    if x>40 and x<70 and y>60 and y<90:
        app.selectedShape='circle'
        app.shapeSelectionLabel=[0,1,0,0,0]
    if x>5 and x<35 and y>100 and y<130:
        app.selectedShape='line'
        app.shapeSelectionLabel=[0,0,1,0,0]
    if x>40 and x<70 and y>100 and y<130:
        app.selectedShape='polygon'
        app.shapeSelectionLabel=[0,0,0,1,0]
    if x>5 and x<35 and y>140 and y<170:
        app.selectedShape='pen'
        app.shapeSelectionLabel=[0,0,0,0,1]
        
def selectColor(app,x,y):
    if x>5 and x<35 and y>290 and y<320:
        app.selectedColor='red'
        app.colorSelectionLabel=[1,0,0,0,0,0,0,0]
    if x>40 and x<70 and y>290 and y<320:
        app.selectedColor='orange'
        app.colorSelectionLabel=[0,1,0,0,0,0,0,0]
    if x>5 and x<35 and y>330 and y<360:
        app.selectedColor='yellow'
        app.colorSelectionLabel=[0,0,1,0,0,0,0,0]
    if x>40 and x<70 and y>330 and y<360:
        app.selectedColor='green'
        app.colorSelectionLabel=[0,0,0,1,0,0,0,0]
    if x>5 and x<35 and y>370 and y<400:
        app.selectedColor='blue'
        app.colorSelectionLabel=[0,0,0,0,1,0,0,0]
    if x>40 and x<70 and y>370 and y<400:
        app.selectedColor='purple'
        app.colorSelectionLabel=[0,0,0,0,0,1,0,0]
    if x>5 and x<35 and y>410 and y<440:
        app.selectedColor='black'
        app.colorSelectionLabel=[0,0,0,0,0,0,1,0]
    if x>40 and x<70 and y>410 and y<440:
        app.selectedColor='gray'
        app.colorSelectionLabel=[0,0,0,0,0,0,0,1]

def main():
    runApp(width=700,height=450)
main()