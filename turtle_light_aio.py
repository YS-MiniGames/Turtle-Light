import math
import turtle

CFG={'canvas':(10000,10000),'bgcolor':(0,0,0),'tracer':16,'async':0}

class Dot:
    def __init__(self,x=0,y=0,color=(255,255,255),width=4):
      self.__x=x
      self.__y=y
      self.__color=color
      self.__width=width
    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @property
    def color(self):
        return self.__color
    @property
    def width(self):
        return self.__width
    def distance(self,other):
        return math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)
    def heading(self,direction,distance=1):
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
        if type(other)==tuple:
            return self.heading(*other)
        return self.heading(other)
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
        turtle.dot(self.width,self.color)
        turtle.penup()

class Line:
    RAYRENDERLEN=1000000000
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
        if self.slope==other.slope:
            return None
        return Dot((other.intercept-self.intercept)/(self.slope-other.slope),(other.intercept-self.intercept)/(self.slope-other.slope)*self.slope+self.intercept)
    def collide(self,other,exact=3):
        if other is None:
            return False
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
            return self.collide(self.collidepoint(other),exact) and other.collide(self.collidepoint(other),exact)
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
        return self.collide(other,2)
    def __or__(self,other):
        return self.collide(other,3)
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
            Line(self.dot1,self.dot1^(self.dot1<<self.dot2,self.RAYRENDERLEN))()
        if self.dotext2:
            Line(self.dot2,self.dot2^(self.dot2<<self.dot1,self.RAYRENDERLEN))()

class Flake:
    def __init__(self,line,reflect=True,transparent=False):
        self.__line=line
        self.__normal=line.direction+math.pi/2
        self.__reflect=reflect
        self.__transparent=transparent
    @property
    def line(self):
        return self.__line
    @property
    def normal(self):
        return self.__normal
    @property
    def reflect(self):
        return self.__reflect
    @property
    def transparent(self):
        return self.__transparent
    def __call__(self,draw,process):
        draw.append(self.line)

class Edge:
    def __init__(self,line,refraction=1):
        self.__line=line
        self.__normal=line.direction+math.pi/2
        self.__refraction=refraction
    @property
    def line(self):
        return self.__line
    @property
    def normal(self):
        return self.__normal
    @property
    def refraction(self):
        return self.__refraction
    def __call__(self,draw,process):
        draw.append(self.line)

ITEMS=(Flake,Edge)

class Light:
    def __init__(self,line,collide=(),refraction=[1],recursion=100):
        self.__source=line.dot1
        self.__line=line
        self.__collide=collide
        self.__refraction=refraction
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
    def ref(self):
        return self.__refraction
    @property
    def ref_last(self):
        return self.__refraction[-1]
    @property
    def rec(self):
        return self.__recursion
    def pass_light(self,item):
        collide_point=self.line@item.line
        return Light(Line(collide_point,collide_point^self.line.direction,False,True,self.line.color,self.line.width),(item,),
                             self.ref,
                             self.rec-1)
    def reflect_light(self,item):
        collide_point=self.line@item.line
        direction=item.normal*2-self.line.direction+math.pi
        return Light(Line(collide_point,collide_point^direction,False,True,self.line.color,self.line.width),(item,),
                             self.ref,
                             self.rec-1)
    def __call__(self,draw,process):
        if self.rec<=0:
            return
        min_item=None
        min_dis=None
        for item in process:
            if type(item) in ITEMS and item not in self.collide:
                collide=self.line@item.line
                if collide is None:
                    continue
                if min_dis is None or collide-self.src<min_dis:
                    min_item=item
                    min_dis=collide-self.src
        item=min_item
        if type(item)==Flake:
            collide_point=self.line@item.line
            draw.append(Line(self.src,collide_point,color=self.line.color,width=self.line.width))
            if item.reflect:
                process.append(self.reflect_light(item))
            if item.transparent:
                process.append(self.pass_light(item))
        elif type(item)==Edge:
            collide_point=self.line@item.line
            draw.append(Line(self.src,collide_point,color=self.line.color,width=self.line.width))
            if item.refraction==self.ref_last:
                nref=self.ref.copy()[:-1]
                sr=self.ref_last
                ir=self.ref[-2]
                p=sr/ir
                theta=math.sin(self.line.direction-item.normal%math.pi)*p
                total_reflect=1<theta%(math.pi*2)<math.pi*2-1
                if total_reflect:
                    process.append(self.reflect_light(item))
                else:
                    process.append(Light(Line(collide_point,collide_point^(math.asin(theta)+item.normal%math.pi),False,True,self.line.color,self.line.width),(item,),
                                         nref,
                                         self.rec-1))
            else:
                nref=self.ref.copy()+[item.refraction]
                sr=self.ref_last
                ir=item.refraction
                p=sr/ir
                theta=math.sin(self.line.direction-item.normal%math.pi)*p
                total_reflect=1<theta%(math.pi*2)<math.pi*2-1
                if total_reflect:
                    process.append(self.reflect_light(item))
                else:
                    process.append(Light(Line(collide_point,collide_point^(math.asin(theta)+item.normal%math.pi),False,True,self.line.color,self.line.width),(item,),
                                         nref,
                                         self.rec-1))
        else:
            draw.append(self.line)

def init(**cfg):
    turtle.clearscreen()
    turtle.speed(0)
    turtle.tracer(cfg['tracer'])
    turtle.radians()
    turtle.colormode(255)
    turtle.screensize(*cfg['canvas'])
    turtle.bgcolor(cfg['bgcolor'])
    turtle.title('Turtle-Light')
    turtle.hideturtle()

def update(*items,**cfg):
    init(**cfg)
    draw_queue=[]
    process_queue=list(items)
    i=0
    while i<len(process_queue):
        process_queue[i](draw_queue,process_queue)
        i+=1
        if cfg['async']==0 or i%cfg['async']==0:
            j=0
            while j<len(draw_queue):
                draw_queue[j]()
                j+=1
            draw_queue=[]
    i=0
    while i<len(draw_queue):
        draw_queue[i]()
        i+=1
