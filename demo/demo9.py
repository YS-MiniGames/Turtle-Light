# 抛物面凸透镜实验
from turtle_light_aio import *
import numpy as np

cfg={'canvas':(100000,100000),'bgcolor':(0,0,0),'tracer':16,'async':1}

lights=[]
s=4
for x in np.arange(-80,80,s):
    light=Light(line=Line(Dot(x,0),Dot(x,1),False,True),
                recursion=100)
    lights.append(light)

lenses=[]
s=0.5
for x in np.arange(-100,100,s):
    lens=Edge(line=Line(Dot(x,400+(x**2-100**2)/200),Dot(x+s,400+((x+s)**2-100**2)/200),False,False,(0,255,255),2),
                refraction=1.2)
    lenses.append(lens)
for x in np.arange(-100,100,s):
    lens=Edge(line=Line(Dot(x,400-(x**2-100**2)/200),Dot(x+s,400-((x+s)**2-100**2)/200),False,False,(0,255,255),2),
                refraction=1.2)
    lenses.append(lens)

update(*lights,*lenses,**cfg)
turtle.mainloop()