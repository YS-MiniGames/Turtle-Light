# 半球面凸透镜成像实验
from turtle_light_aio import *
import numpy as np

cfg={'canvas':(100000,100000),'bgcolor':(0,0,0),'tracer':16,'async':1}

lights=[]
s=0.008
for theta in np.arange(1,math.pi-1,s):
    light=Light(line=Line(Dot(0,0),Dot(0,0)^(theta),False,True,(255,255,255),1),
                recursion=100)
    lights.append(light)

lenses=[]
s=0.008
for theta in np.arange(-math.pi,0,s):
    lens=Edge(line=Line(Dot(0,500)^(theta,100),Dot(0,500)^(theta+s,100),False,False,(0,255,255),2),
                refraction=1.2)
    lenses.append(lens)
lenses.append(Edge(line=Line(Dot(-100,500),Dot(100,500),False,False,(0,255,255),2),
                refraction=1.2))

wall=Flake(line=Line(Dot(-100,800),Dot(100,800),False,False,(255,0,0),2),reflect=False,transparent=False)
update(*lights,*lenses,wall,**cfg)
turtle.mainloop()