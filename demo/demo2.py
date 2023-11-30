# 半球面凸透镜实验
from turtle_light_aio import *
import numpy as np

cfg={'canvas':(100000,100000),'bgcolor':(0,0,0),'tracer':64,'async':0}

lights=[]
s=0.01
for x in np.arange(-80,80,s):
    light=Light(line=Line(Dot(x,0),Dot(x,1),False,True),
                recursion=100)
    lights.append(light)

lenses=[]
s=0.008
for theta in np.arange(-math.pi,0,s):
    lens=Edge(line=Line(Dot(0,400)^(theta,100),Dot(0,400)^(theta+s,100),False,False,(0,255,255),2),
                refraction=6)
    lenses.append(lens)
lenses.append(Edge(line=Line(Dot(100,400),Dot(-100,400),False,False,(0,255,255),2),
                refraction=6))

update(*lights,*lenses,**cfg)
turtle.mainloop()