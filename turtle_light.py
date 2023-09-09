import math
import turtle

INF=40000

class Dot:
    def __init__(self,x=0,y=0,color=(255,255,255)):
      self.__x=x
      self.__y=y
      self.__color=color
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def color(self):
        return self.__color
    def distance(self,other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
    def heading(self,direction,distance):
        x=self.x+math.cos(direction)*distance
        y=self.y+math.sin(direction)*distance
        return Dot(x,y)
    def towards(self,other):
        if self.x>other.x:
            return math.pi-math.asin((other.y-self.y)/self.distance(other))
        return math.asin((other.y-self.y)/self.distance(other))
    def __repr__(self):
        return '({x},{y})'.format(x=self.x,y=self.y)
    def __eq__(self,other):
        return self.x==other.x and self.y==other.y
    def __or__(self,other):
        return self.distance(other)<0.1
    def __sub__(self,other):
        return self.distance(other)
    def __xor__(self,other):
        return self.heading(*other)
    def __lshift__(self,other):
        return other.towards(self)
    def __rshift__(self,other):
        return self.towards(other)
    def __abs__(self):
        return self.distance(Dot(0,0))
    def __tuple__(self):
        return self.x,self.y
    def __call__(self):
        turtle.penup()
        turtle.pencolor(self.color)
        turtle.goto(self.x,self.y)
        turtle.pendown()
        turtle.dot()
        turtle.penup()

class Line:
    def __init__(self,dot1=Dot(),dot2=Dot(1,0),dotext1=False,dotext2=False,color=(255,255,255),width=1):
        self.__dot1=dot1
        self.__dot2=dot2
        self.__dotext1=dotext1
        self.__dotext2=dotext2
        self.__color=color
        self.__width=width
    @property
    def dot1(self):
        return self.__dot1
    @property
    def dot2(self):
        return self.__dot2
    @property
    def dotext1(self):
        return self.__dotext1
    @property
    def dotext2(self):
        return self.__dotext2
    @property
    def color(self):
        return self.__color
    @property
    def width(self):
        return self.__width
    @property
    def direction(self):
        return self.dot1>>self.dot2
    @property
    def slope(self):
        if self.dot1.x==self.dot2.x:
            return None
        return (self.dot1.y-self.dot2.y)/(self.dot1.x-self.dot2.x)
    @property
    def vertical(self):
        return self.slope is None
    @property
    def intercept(self):
        if self.vertical:
            return self.dot1.x
        return self.dot1.y-self.dot1.x*self.slope
    @property
    def x_min(self):
        dot1=self.dot1.x
        dot2=self.dot2.x
        dotext1=self.dotext1
        dotext2=self.dotext2
        if dot1>dot2:
            dot1,dot2=dot2,dot1
            dotext1,dotext2=dotext2,dotext1
        if dotext1:
            return None
        return dot1
    @property
    def y_min(self):
        dot1=self.dot1.y
        dot2=self.dot2.y
        dotext1=self.dotext1
        dotext2=self.dotext2
        if dot1>dot2:
            dot1,dot2=dot2,dot1
            dotext1,dotext2=dotext2,dotext1
        if dotext1:
            return None
        return dot1
    @property
    def x_max(self):
        dot1=self.dot1.x
        dot2=self.dot2.x
        dotext1=self.dotext1
        dotext2=self.dotext2
        if dot1>dot2:
            dot1,dot2=dot2,dot1
            dotext1,dotext2=dotext2,dotext1
        if dotext2:
            return None
        return dot2
    @property
    def y_max(self):
        dot1=self.dot1.y
        dot2=self.dot2.y
        dotext1=self.dotext1
        dotext2=self.dotext2
        if dot1>dot2:
            dot1,dot2=dot2,dot1
            dotext1,dotext2=dotext2,dotext1
        if dotext2:
            return None
        return dot2
    def collidepoint(self,other):
        if self.vertical:
            if other.vertical:
                return None
            return Dot(self.intercept,other.slope*self.intercept+other.intercept)
        if other.vertical:
            return Dot(other.intercept,self.slope*other.intercept+self.intercept)
        return Dot((other.intercept-self.intercept)/(self.slope-other.slope),(other.intercept-self.intercept)/(self.slope-other.slope)*self.slope+self.intercept)
    def collide(self,other,exact=3):
        if type(other)==Dot:
            collidex=(self.x_min is None or other.x>=self.x_min) and (self.x_max is None or other.x<=self.x_max)
            collidey=(self.y_min is None or other.y>=self.y_min) and (self.y_max is None or other.y<=self.y_max)
            if exact==0:
                return collidex and collidey and other.y==other.x*self.slope+self.intercept
            if exact==1:
                return collidex and collidey and -0.1<other.y-other.x*self.slope-self.intercept<0.1
            if exact==2:
                return collidex and collidey
            if exact==3:
                return (self.vertical and collidey) or ((not self.vertical) and collidex)
            if exact==4:
                return collidex or collidey
        if type(other)==Line:
            return self.collide(self.collidepoint(other)) and other.collide(self.collidepoint(other))
    def __repr__(self):
        if self.vertical:
            if self.y_min is None:
                if self.y_max is None:
                    return 'x={x}'.format(x=self.intercept)
                return 'x={x},y<={ymax}'.format(x=self.intercept,ymax=self.y_max)
            if self.y_max is None:
                return 'x={x},y>={ymin}'.format(x=self.intercept,ymin=self.y_min)
            return 'x={x},{ymin}<=y<={ymax}'.format(x=self.intercept,ymin=self.y_min,ymax=self.y_max)
        if self.x_min is None:
            if self.x_max is None:
                return 'y={k}x+{b}'.format(k=self.slope,b=self.intercept)
            return 'y={k}x+{b},x<={xmax}'.format(k=self.slope,b=self.intercept,xmax=self.x_max)
        if self.y_max is None:
            return 'y={k}x+{b},{xmin}<=x'.format(k=self.slope,b=self.intercept,xmin=self.x_min)
        return 'y={k}x+{b},{xmin}<=x<={xmax}'.format(k=self.slope,b=self.intercept,xmin=self.x_min,xmax=self.x_max)
    def __eq__(self,other):
        return self.collide(other,True)
    def __or__(self,other):
        return self.collide(other,False)
    def __xor__(self,other):
        return self.collide(other)
    def __and__(self,other):
        return self.collidepoint(other)
    def __matmul__(self,other):
        if self.collide(other):
            return self.collidepoint(other)
        return None
    def __call__(self):
        turtle.penup()
        turtle.pencolor(self.color)
        turtle.pensize(self.width)
        turtle.goto(self.dot1.x,self.dot1.y)
        turtle.pendown()
        turtle.goto(self.dot2.x,self.dot2.y)
        turtle.penup()
        if self.dotext1:
            Line(self.dot1,self.dot1^(self.dot1<<self.dot2,INF))()
        if self.dotext2:
            Line(self.dot2,self.dot2^(self.dot2<<self.dot1,INF))()

class Mirror:
    def __init__(self,line):
        self.__line=line
        self.__normal=line.direction+math.pi
    @property
    def line(self):
        return self.__line
    @property
    def normal(self):
        return self.__normal
    def __call__(self,draw,process):
        draw.append(self.line)

class Light:
    def __init__(self,source=Dot(),direction=0,color=(255,255,255),width=1,collide=(),recursion=100):
        self.__source=source
        self.__line=Line(source,source^(direction,1),False,True,color,width)
        self.__collide=collide
        self.__recursion=recursion
    @property
    def src(self):
        return self.__source
    @property
    def line(self):
        return self.__line
    @property
    def collide(self):
        return self.__collide
    @property
    def rec(self):
        return self.__recursion
    def __call__(self,draw,process):
        min_item=None
        min_dis=INF
        for item in process:
            if type(item) in (Mirror,) and item not in self.collide:
                collide=self.line@item.line
                if collide is None:
                    continue
                if collide-self.src<min_dis:
                    min_item=item
                    min_dis=collide-self.src
        item=min_item
        if type(item)==Mirror:
            draw.append(Line(self.src,self.line@item.line,color=self.line.color))
            process.append(Light(self.line@item.line,item.normal*2-self.line.direction,self.line.color,self.line.width,(item,),self.rec-1))
        else:
            draw.append(Line(self.src,self.line.dot2,False,True,self.line.color))

def init():
    turtle.clearscreen()
    turtle.speed(0)
    turtle.tracer(4)
    turtle.colormode(255)
    turtle.radians()
    turtle.screensize(10000,10000)
    turtle.bgcolor((0,0,0))
    turtle.title('Turtle-Light')
    turtle.hideturtle()
    turtle.pensize(1)
    turtle.pencolor((255,255,255))

def update(*items):
    init()
    draw_queue=[]
    process_queue=list(items)
    i=0
    while i<len(process_queue):
        process_queue[i](draw_queue,process_queue)
        i+=1
    i=0
    while i<len(draw_queue):
        draw_queue[i]()
        i+=1