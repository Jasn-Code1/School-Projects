import pygame as pg
import numpy as np
import math as m
import random as rand
from sys import exit

pg.init()

def lerp2d(a,b,t):
    return [a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t]

def bcurve3(p,p1,p2,t):
    p3=lerp2d(p,p1,t)
    p4=lerp2d(p1,p2,t)
    p5=lerp2d(p3,p4,t)
    return p5

def bcurve4(p,p1,p2,p3,t):
    p4=lerp2d(p,p1,t)
    p5=lerp2d(p1,p2,t)
    p6=lerp2d(p2,p3,t)
    p7=lerp2d(p4,p5,t)
    p8=lerp2d(p5,p6,t)
    p9=lerp2d(p7,p8,t)
    return p9

class Textclass:
    def __init__(self,text,position,initial_position,third_position,color,size,interval):
        self.interval=interval
        self.txt=text
        self.font=pg.font.Font(None,size)
        self.font.italic=True
        self.surf=self.font.render(self.txt,True,color)
        self.position=position
        self.initial_position=initial_position
        self.rect=self.surf.get_rect(midbottom=self.initial_position)
        self.third_position=third_position
        self.i=0
        self.color=color
    def update(self,fps):
        if self.i<self.interval:
            self.i+=50/fps
        else:
            self.i=self.interval
        self.surf=self.font.render(self.txt,True,self.color)
        pos=bcurve3(self.initial_position,self.third_position,self.position,self.i/self.interval)
        self.rect=self.surf.get_rect(midbottom=(self.position[0],pos[1]))
    def draw(self,surface):
        surface.blit(self.surf,self.rect)

class Textclass1:
    def __init__(self,text,position,color,size):
        self.txt=text
        self.txt1=self.txt[round((len(self.txt)-1)/2)]
        self.font=pg.font.Font(None,size)
        self.font.italic=True
        self.surf=self.font.render(self.txt1,True,color)
        self.position=position
        self.rect=self.surf.get_rect(midbottom=self.position)
        self.color=color
        self.i=0
    def update(self,fps):
        self.txt1=self.txt[round((len(self.txt)-1)/2)-(m.floor(self.i-1)//2):round((len(self.txt)-1)/2)+(m.floor(self.i+2)//2)]
        self.surf=self.font.render(self.txt1,True,self.color)
        self.rect=self.surf.get_rect(midbottom=self.position)
        if self.i+20/fps<len(self.txt):
            self.i+=20/fps
        else:
            self.i=len(self.txt)
    def draw(self,surface):
        surface.blit(self.surf,self.rect)

class Textbox:
    def __init__(self,position,size,font_size):
        self.surf=pg.surface.Surface(size)
        self.surf.fill((0,255,0))
        self.surf1=pg.surface.Surface(np.subtract(size,(2,2)))
        self.surf1.fill('black')
        self.surf.blit(self.surf1,(1,1))
        self.surf2=self.surf.copy()
        self.position=position
        self.size=size
        self.font_size=font_size
        self.rect=self.surf2.get_rect(midbottom=self.position)
        self.text=""
        self.issellected=False
        self.i=0
        self.j=0
    def update(self,fps):
        if self.i+300/fps<self.size[0]:
            self.i+=300/fps
        else:
            self.i=self.size[0]
        if self.j+300/fps<self.size[1]:
            self.j+=300/fps
        else:
            self.j=self.size[1]
        self.surf=pg.surface.Surface((round(self.i),round(self.j)))
        if self.issellected:
            self.surf.fill((255,255,255))
        else:
            self.surf.fill((0,255,0))
        self.surf1=pg.surface.Surface(np.subtract((round(self.i),round(self.j)),(2,2)))
        self.surf1.fill('black')
        self.surf.blit(self.surf1,(1,1))
        self.surf2=self.surf.copy()
        self.rect=self.surf2.get_rect(midbottom=self.position)
    def mousedown(self,pos):
        if self.rect.collidepoint(pos):
            self.issellected=True
        else:
            self.issellected=False
    def keydown(self,unicode,key):
        if self.issellected:
            if key==pg.K_BACKSPACE:
                if len(self.text)>0:
                    self.text=self.text[:len(self.text)-1]
            if unicode.isdigit():
                self.text+=unicode
    def draw(self,surface):
        self.surf2.blit(self.surf,(0,0))
        self.font=pg.font.Font(None,self.font_size)
        self.txt_surf=self.font.render(self.text,True,'white')
        self.txt_rect=self.txt_surf.get_rect(center=(round(self.size[0]/2),round(self.size[1]/2)))
        self.surf2.blit(self.txt_surf,self.txt_rect)
        surface.blit(self.surf2,self.rect)

class Button:
    def __init__(self,position,size,font_size,text,color):
        self.surf=pg.surface.Surface(size)
        self.surf.fill((0,255,0))
        self.surf1=pg.surface.Surface(np.subtract(size,(4,4)))
        self.surf1.fill(color)
        self.surf.blit(self.surf1,(2,2))
        self.clicked=False
        self.isup=False
        self.position=position
        self.rect=self.surf.get_rect(midbottom=self.position)
        self.size=size
        self.font_size=font_size
        self.i=0
        self.j=0
        self.text=text
        self.color=color
        if self.i==self.size[0]:
            self.font=pg.font.Font(None,self.font_size)
            self.txt=self.font.render(self.text,True,"white")
            self.txt_rect=self.txt.get_rect(center=(round(self.size[0]/2),round(self.size[1]/2)))
            self.surf.blit(self.txt,self.txt_rect)
    def update(self,fps):
        if self.i+300/fps<self.size[0]:
            self.i+=300/fps
        else:
            self.i=self.size[0]
        if self.j+300/fps<self.size[1]:
            self.j+=300/fps
        else:
            self.j=self.size[1]
        size=(self.i,self.j)
        if self.isup:
            self.surf=pg.surface.Surface(size)
            self.surf.fill((255,255,255))
            self.surf1=pg.surface.Surface(np.subtract(size,(4,4)))
            self.surf1.fill(self.color)
            self.surf.blit(self.surf1,(2,2))
            self.rect=self.surf.get_rect(midbottom=self.position)
            if self.i==self.size[0]:
                self.font=pg.font.Font(None,self.font_size)
                self.txt=self.font.render(self.text,True,"white")
                self.txt_rect=self.txt.get_rect(center=(round(size[0]/2),round(size[1]/2)))
                self.surf.blit(self.txt,self.txt_rect)
        else:
            self.surf=pg.surface.Surface(size)
            self.surf.fill((0,255,0))
            self.surf1=pg.surface.Surface(np.subtract(size,(4,4)))
            self.surf1.fill(self.color)
            self.surf.blit(self.surf1,(2,2))
            self.rect=self.surf.get_rect(midbottom=self.position)
            if self.i==self.size[0]:
                self.font=pg.font.Font(None,self.font_size)
                self.txt=self.font.render(self.text,True,"white")
                self.txt_rect=self.txt.get_rect(center=(round(size[0]/2),round(size[1]/2)))
                self.surf.blit(self.txt,self.txt_rect)
        if self.clicked:
            self.clicked=False
    def mousedown(self,pos):
        if self.rect.collidepoint(pos):
            self.isup=True
    def mouseup(self,pos):
        if self.rect.collidepoint(pos) and self.isup:
            self.clicked=True
            self.isup=False
    def draw(self,surface):
        surface.blit(self.surf,self.rect)

class Card:
    def __init__(self,position):
        self.surf=pg.surface.Surface((600,280))
        self.surf.fill('black')
        self.position=position
        self.rect=self.surf.get_rect(midtop=self.position)
        self.i=0
        self.init_pos=(300,0)
        self.init_pos1=(300,0)
        self.color=[0,255,0]
        self.bool=True
        self.j=0
        self.surf1=self.surf.copy()
        self.counter=0
        self.person=[]
        self.Group=pg.sprite.Group()
        self.count=0
    def update(self,fps):
        global running
        if self.j<3:
            if self.i<100:
                self.i+=150/fps
                if self.i>=100:
                    self.i=100
            else:
                self.i=0
                self.j+=1
        if self.j==0:
            pos=lerp2d((299,0),(0,0),self.i/100)
            pos1=lerp2d((300,0),(599,0),self.i/100)
        elif self.j==1:
            pos=lerp2d((0,0),(0,279),self.i/100)
            pos1=lerp2d((599,0),(599,279),self.i/100)
        elif self.j==2:
            pos=lerp2d((0,279),(299,279),self.i/100)
            pos1=lerp2d((599,279),(300,279),self.i/100)
            if self.i==100:
                self.surf1=self.surf.copy()
                self.txt=Textclass1('Enter your card number:',(300,50),(255,255,255),45)
                self.txt_box=Textbox((300,90),(400,35),30)
                self.txt1=Textclass1('Enter your pin number:',(300,150),(255,255,255),45)
                self.txt_box1=Textbox((300,190),(400,35),30)
                self.btn=Button((430,250),(70,40),30,'Login',(0,50,50))
                self.btn1=Button((520,250),(70,40),30,'Exit',(50,0,0))
        if self.j<3:
            pg.draw.line(self.surf,self.color,pos,self.init_pos,5)
            pg.draw.line(self.surf,self.color,pos1,self.init_pos1,5)
            self.init_pos=pos
            self.init_pos1=pos1
        if self.bool and self.color[2]<255:
            self.color[2]+=round(100/fps)
            if self.color[2]>255:
                self.color[2]=255
        elif (not self.bool) and self.color[2]>0:
            self.color[2]-=round(100/fps)
            if self.color[2]<0:
                self.color[2]=0
        else:
            self.bool=False if self.bool else True
        if self.j==3:
            if self.btn1.clicked:
                running=False
            if self.btn.clicked:
                cn=False
                pn=False
                for person in info:
                    if self.txt_box.text==person[1]:
                        cn=True
                    if self.txt_box1.text==person[2]:
                        pn=True
                        if cn:
                            global txt2,asctxt
                            self.person=person
                            txt2=Textclass('User: ',(sc_width/2,105),(sc_width/2,-100),(sc_width/2+200,175),(200,100,255),30,100)
                            txt2.txt='User: '+person[0]
                            asctxt=Ascending()
                            break
                global page
                global warning_message
                if pn and cn:
                    page=1
                elif self.txt_box.text=='':
                    page=2
                    warning_message='Card number must be filled in!'
                    self.txt_box.issellected=True
                elif self.txt_box1.text=='':
                    page=2
                    warning_message='Pin number must be filled in!'
                    self.txt_box1.issellected=True
                elif not cn:
                    page=2
                    warning_message="Card number doesn't exist, Try again!"
                    self.txt_box.issellected=True
                    self.txt_box.text=''
                    self.txt_box1.text=''
                else:
                    page=2
                    warning_message='Wrong Pin number, Try again!'
                    self.txt_box1.issellected=True
                    self.txt_box1.text=''
        if self.j==3:
            if self.count<2:
                self.count+=1
            else:
                r=rand.randint(0,600)
                self.Group.add(Design1((r,0),(r,500),(0,255,255),50,1))
                self.count=0
    def mousedown(self,pos):
        if self.j==3:
            self.txt_box.mousedown(np.subtract(pos,self.rect.topleft))
            self.txt_box1.mousedown(np.subtract(pos,self.rect.topleft))
            self.btn.mousedown(np.subtract(pos,self.rect.topleft))
            self.btn1.mousedown(np.subtract(pos,self.rect.topleft))
    def mouseup(self,pos):
        if self.j==3:
            self.btn.mouseup(np.subtract(pos,self.rect.topleft))
            self.btn1.mouseup(np.subtract(pos,self.rect.topleft))
    def keydown(self,unicode,key):
        if self.j==3:
            self.txt_box.keydown(unicode,key)
            self.txt_box1.keydown(unicode,key)
    def draw(self,surface):
        if self.j==3:
            self.surf1.blit(self.surf,(0,0))
            self.Group.update(self.surf1,fps)
            self.Group.draw(self.surf1)
            self.txt.update(fps)
            self.txt_box.update(fps)
            self.txt.draw(self.surf1)
            self.txt_box.draw(self.surf1)
            if self.counter<2:
                self.counter+=1/fps
            if self.counter>=1:
                self.txt1.update(fps)
                self.txt_box1.update(fps)
                self.txt1.draw(self.surf1)
                self.txt_box1.draw(self.surf1)
            if self.counter>=2:
                self.btn.update(fps)
                self.btn1.update(fps)
                self.btn.draw(self.surf1)
                self.btn1.draw(self.surf1)
            surface.blit(self.surf1,self.rect)
        else:
            surface.blit(self.surf,self.rect)

class Warning:
    def __init__(self):
        self.surf=pg.surface.Surface((400,200))
        self.rect=self.surf.get_rect(center=(sc_width/2,sc_height/2))
        self.surf1=pg.surface.Surface((395,195))
        self.rect1=self.surf1.get_rect(center=(sc_width/2,sc_height/2))
        self.btn=Button((sc_width/2,290),(60,40),35,'OK',(50,50,50))
    def update(self):
        if self.btn.clicked:
            global page
            page=0
            self.btn=Button((sc_width/2,280),(60,40),35,'OK',(50,50,50))
    def mousedown(self,pos):
        self.btn.mousedown(pos)
    def mouseup(self,pos):
        self.btn.mouseup(pos)
    def draw(self,surface):
        pg.draw.rect(surface,(255,0,0),self.rect,0,20)
        pg.draw.rect(surface,(20,20,20),self.rect1,0,20)
        self.font=pg.font.Font(None,30)
        self.txt=self.font.render(warning_message,True,"white")
        self.txt_rect=self.txt.get_rect(center=(sc_width/2,sc_height/2-20))
        surface.blit(self.txt,self.txt_rect)
        self.btn.update(fps)
        self.btn.draw(surface)

class Ascending:
    def __init__(self):
        self.textlist=[
            '1.Deposit',
            '2.Withdrawal',
            '3.Balance Ing',
            '4.Fund Transfer',
            '5.Mini Statement',
            '6.Change Pin',
            '7.Last 5 Transactions',
            '8.Logout'
        ]
        self.initial_position=[]
        self.middle_position=[]
        self.positions=[]
        self.used_positions=[]
        self.rects=[]
        self.surfs=[]
        self.font=pg.font.Font(None,35)
        for i in range(8):
            self.positions.append((120+i//4*200,180+i*40-4*40*(i//4)))
            self.initial_position.append(np.add(self.positions[i],(-600+1200*(i//4),0)))
            self.used_positions.append(self.initial_position[i])
            self.middle_position.append(np.add(self.positions[i],(0,500)))
            self.surfs.append(self.font.render(self.textlist[i],True,(255-(i*61 if i<4 else 255),255,255-((i-4)*61) if i>3 else 255)))
            self.rects.append(self.surfs[i].get_rect(midleft=self.initial_position[i]))
        self.i=0
    def update(self,fps):
        if self.i+30/fps<100:
            self.i+=30/fps
        else:
            self.i=100
        for i in range(8):
            pos=bcurve3(self.initial_position[i],self.middle_position[i],self.positions[i],self.i/(100-abs(i-4)*20) if self.i/(100-abs(i-4)*20)<1 else 1)
            self.used_positions[i]=(pos[0],self.positions[i][1])
            self.rects[i]=self.surfs[i].get_rect(midleft=self.used_positions[i])
    def draw(self,surface):
        for i in range(8):
            surface.blit(self.surfs[i],self.rects[i])

class Design:
    def __init__(self):
        self.rad=0
        self.color=[255,0,255]
        self.color1=[255,255,255]
        self.color_speed=55
        self.color_speed1=55
        self.bool=False
        self.bool1=False
    def update(self,fps):
        if self.rad+m.pi/4/fps<2*m.pi:
            self.rad+=m.pi/4/fps
        else:
            self.rad-=2*m.pi
        if self.bool and self.color[0]<255:
            self.color[0]+=round(self.color_speed1/fps)
            if self.color[0]>=255:
                self.color[0]=255
                self.bool=False
        elif self.color[0]>0:
            self.color[0]-=round(self.color_speed1/fps)
            if self.color[0]<=0:
                self.color[0]=0
                self.bool=True

        if self.bool and self.color1[0]<255:
            self.color1[0]+=round(self.color_speed/fps)
            if self.color1[0]>=255:
                self.color1[0]=255
                self.bool=False
            self.color1[2]=self.color1[0]
        elif self.color1[0]>0:
            self.color1[0]-=round(self.color_speed/fps)
            if self.color1[0]<=0:
                self.color1[0]=0
                self.bool=True
            self.color1[2]=self.color1[0]
    def draw(self,surface):
        lines=[]
        lines1=[]
        for i in range(320):
            lines.append((i*2,50+40*m.sin(i*m.pi/180+self.rad)))
            lines1.append((i*2,50+40*m.cos(5*i*m.pi/180/3+self.rad)))
        pg.draw.lines(surface,'white',False,lines,7)
        pg.draw.lines(surface,'white',False,lines1,7)
        pg.draw.lines(surface,self.color,False,lines,5)
        pg.draw.lines(surface,self.color1,False,lines1,5)

class Design1(pg.sprite.Sprite):
    def __init__(self,position,end_position,color,speed,radius):
        super().__init__()
        self.position=position
        self.end_position=end_position
        self.speed=speed
        self.color=color
        self.radius=radius
        self.image=pg.surface.Surface((radius*2,2*radius))
        pg.draw.circle(self.image,color,(radius,radius),radius)
        diff=np.subtract(self.end_position,self.position)
        self.rad=m.atan2(diff[1],diff[0])
        self.rect=self.image.get_rect(center=self.position)
        self.ranint=rand.randint(10,100)
        self.lines=[]
        self.color=[0,rand.randint(0,255),rand.randint(0,255)]
        self.surf=pg.surface.Surface((radius*4,4*radius))
        pg.draw.circle(self.surf,'white',(self.radius*2,2*self.radius),self.radius*2)
        self.surf.convert_alpha()
        self.surf.set_alpha(200)
        self.srect=self.surf.get_rect(center=self.position)
    def update(self,surface,fps):
        diff=np.subtract(self.end_position,self.position)
        hyp=(np.sum(np.square(diff)))**.5
        if hyp>20:
            self.position=np.add(self.position,np.divide(np.multiply(self.speed,(m.cos(self.rad),m.sin(self.rad))),fps))
            self.rect=self.image.get_rect(center=self.position)
        else:
            self.kill()
        if len(self.lines)<self.ranint:
            self.lines.append(self.position)
        else:
            self.lines.pop(0)
            self.lines.append(self.position)
        if len(self.lines)>1:
            pg.draw.lines(surface,self.color,False,self.lines,1)
        self.srect=self.surf.get_rect(center=self.position)
        surface.blit(self.surf,self.srect)

class Design2:
    def __init__(self,x,speed):
        self.x=x
        self.points=[
            [x,-100],
            [x,-100],
            [x,-100],
            [x,0],
            [x,400],
            [x,400]
        ]
        self.points1=[
            [x,-100],
            [x,-100],
            [x,-100],
            [x,0],
            [x,400],
            [x,400]
        ]
        self.x=x
        for i in range(7):
            r=rand.randint(-50,50)
            if x<100:
                self.points.insert(-2,[self.x+50+r,50+50*i])
                self.points1.insert(-2,[self.x+50+r,50+50*i])
            else:
                self.points.insert(-2,[self.x-50+r,50+50*i])
                self.points1.insert(-2,[self.x-50+r,50+50*i])
        self.color=[255,255,255]
        self.bool=False
        self.speed=speed
        self.color_speed=40
    def update(self,fps):
        for i in range(len(self.points)):
            diff=np.subtract(self.points[i],self.points1[i])
            rad=m.atan2(diff[1],diff[0])
            hyp=(np.sum(np.square(diff)))**.5
            if hyp>self.speed/fps:
                self.points1[i]=np.add(self.points1[i],np.divide(np.multiply(self.speed,(m.cos(rad),m.sin(rad))),fps))
            else:
                self.points1[i]=self.points[i]
                r=rand.randint(-50,50)
                if self.x<100:
                    self.points[i]=[self.x+50+r,self.points[i][1]]
                else:
                    self.points[i]=[self.x-50+r,self.points[i][1]]
        if self.bool and self.color[0]<255:
            self.color[0]+=round(self.color_speed/fps)
            if self.color[0]>=255:
                self.color[0]=255
                self.bool=False
            self.color[2]=self.color[0]
        elif self.color[0]>0:
            self.color[0]-=round(self.color_speed/fps)
            if self.color[0]<=0:
                self.color[0]=0
                self.bool=True
            self.color[2]=self.color[0]
    def draw(self,surface):
        self.lines=[]
        for t in range(101):
            self.line=[]
            for i in range(4):
                self.line.append(bcurve4(self.points1[i*3],self.points1[i*3+1],self.points1[i*3+2],lerp2d(self.points1[i*3+2],self.points1[i*3+3],.5),t/100))
            self.lines.append(self.line)
        self.lines1=[]
        for i in range(len(self.lines[0])):
            for ln in self.lines:
                self.lines1.append(ln[i])
        pg.draw.lines(surface,self.color,False,self.lines1,7)
        pg.draw.lines(surface,'white',False,self.lines1,3)

class Design3:
    def __init__(self,position,size):
        self.text=''
        self.text1=''
        self.i=0
        self.ch=32
        self.font=pg.font.Font(None,size)
        self.position=position
    def load(self,text):
        self.text=text
    def update(self,fps):
        for _ in range(10):
            if self.i<len(self.text):
                if self.ch==32:
                    self.text1=self.text1+' '
                if self.ch<147:
                    self.ch+=1
                else:
                    self.ch=32
                if self.ch==32 and self.text[self.i]==' ':
                    self.i+=1
                    self.text1=self.text1[:len(self.text1)-1]+' '
                    self.ch=32
                elif self.text[self.i]==chr(self.ch):
                    self.i+=1
                    self.text1=self.text1[:len(self.text1)-1]+chr(self.ch)
                    self.ch=32
                else:
                    if self.ch!=32:
                        self.text1=self.text1[:len(self.text1)-1]+chr(self.ch)
                self.surf=self.font.render(self.text1,True,(255,255,255))
                self.rect=self.surf.get_rect(center=self.position)
    def draw(self,surface):
        surface.blit(self.surf,self.rect)
    
class Design4(pg.sprite.Sprite):
    def __init__(self,position,end_position,speed):
        super().__init__()
        self.position=position
        self.end_position=end_position
        self.font=pg.font.Font(None,20)
        self.color=[0,rand.randint(0,255),rand.randint(0,255)]
        self.surf_list=[]
        self.image=self.font.render(chr(rand.randint(33,122)),True,self.color)
        self.rect=self.image.get_rect(center=self.position)
        self.speed=speed
        self.length=rand.randint(4,10)
        diff=np.subtract(self.end_position,self.position)
        self.rad=m.atan2(diff[1],diff[0])
        self.counter=0
    def update(self,surface,fps):
        diff=np.subtract(self.end_position,self.position)
        hyp=(np.sum(np.square(diff)))**.5
        if hyp>20:
            self.position=np.add(self.position,np.divide(np.multiply(self.speed,(m.cos(self.rad),m.sin(self.rad))),fps))
            self.rect=self.image.get_rect(center=self.position)
        else:
            self.kill()
        if self.counter<.2:
            self.counter+=1/fps
        else:
            if len(self.surf_list)<self.length:
                ch=self.font.render(chr(rand.randint(33,122)),True,[0,rand.randint(0,255),rand.randint(0,255)])
                rect=ch.get_rect(center=self.position)
                self.surf_list.append((ch,rect))
            else:
                self.surf_list.pop(0)
                ch=self.font.render(chr(rand.randint(33,122)),True,[0,rand.randint(0,255),rand.randint(0,255)])
                rect=ch.get_rect(center=self.position)
                self.surf_list.append((ch,rect))
            self.counter=0
        for surf,rect in self.surf_list:
            surface.blit(surf,rect)

def Indicator(key):
    global page
    if key==pg.K_8:
        page=0
        card.txt_box.text=''
        card.txt_box1.text=''
    if key==pg.K_3:
        global design3,design4,count1
        page=3
        design3=Design3((sc_width/2,200),45)
        design4=Design3((sc_width/2,300),30)
        design3.text='Your balance is: $'+card.person[3]
        design4.text='Press < 1 > to go back...'
        txt_group.empty()
        count1=0
    if page==3 and key==pg.K_1:
        page=1

pg.display.set_caption('Bank of PANDORA')
screen=pg.display.set_mode((640, 400))
sc_width,sc_height=screen.get_size()
clock=pg.time.Clock()

txt=Textclass('Welcome to',(sc_width/2,40),(sc_width/2,-200),(sc_width/2+200,100),(0,255,0),35,130)
txt_1=Textclass('Welcome to',(sc_width/2,40),(sc_width/2,-200),(sc_width/2+200,100),(0,50,0),41,130)
txt1=Textclass('Bank of PANDORA',(sc_width/2,80),(sc_width/2,-100),(sc_width/2+200,150),(0,200,255),50,120)
txt1_1=Textclass('Bank of PANDORA',(sc_width/2,80),(sc_width/2,-100),(sc_width/2+200,150),(50,0,100),56,100)
txt2=Textclass('User: ',(sc_width/2,105),(sc_width/2,-100),(sc_width/2+200,175),(200,100,255),30,100)

card=Card((sc_width/2,100))
design=Design()
design1=Design2(0,20)
design2=Design2(640,20)
design3=Design3((sc_width/2,200),45)
design4=Design3((sc_width/2,300),30)

txt_group=pg.sprite.Group()

warning=Warning()
asctxt=Ascending()

info=[
    ['Poge Harvie','12345','6789','148.75']
    ]

count=0
count1=0

warning_message=''
page=0
running=True
while running:
    fps=clock.get_fps()
    fps=60 if fps==0 else fps
    for e in pg.event.get():
        if e.type==pg.QUIT:
            running=False
        if e.type==pg.KEYDOWN:
            if e.key==pg.K_ESCAPE:
                running=False
            if page==0:
                card.keydown(e.unicode,e.key)
        if page==0:
            if e.type==pg.MOUSEBUTTONDOWN:
                card.mousedown(e.pos)
            if e.type==pg.MOUSEBUTTONUP:
                card.mouseup(e.pos)
        elif page==1:
            if e.type==pg.KEYDOWN:
                Indicator(e.key)
        elif page==2:
            if e.type==pg.MOUSEBUTTONDOWN:
                warning.mousedown(e.pos)
            if e.type==pg.MOUSEBUTTONUP:
                warning.mouseup(e.pos)
        elif page==3:
            if e.type==pg.KEYDOWN:
                Indicator(e.key)

    if page==0:
        screen.fill('black')

        design.update(fps)
        txt_1.update(fps)
        txt.update(fps)
        txt1_1.update(fps)
        txt1.update(fps)
        card.update(fps)

        design.draw(screen)
        txt_1.draw(screen)
        txt.draw(screen)
        txt1_1.draw(screen)
        txt1.draw(screen)
        card.draw(screen)
    elif page==1:
        screen.fill('black')

        design1.update(fps)
        design2.update(fps)
        txt_1.update(fps)
        txt.update(fps)
        txt1_1.update(fps)
        txt1.update(fps)
        txt2.update(fps)
        asctxt.update(fps)

        design1.draw(screen)
        design2.draw(screen)
        txt_1.draw(screen)
        txt.draw(screen)
        txt1_1.draw(screen)
        txt1.draw(screen)
        txt2.draw(screen)
        asctxt.draw(screen)
    elif page==2:
        warning.update()
        warning.draw(screen)
    elif page==3:
        r=rand.randint(0,640)
        if count<4:
            count+=1
        else:
            count=0
            txt_group.add(Design4((r,0),(r,600),50))
        screen.fill('black')

        txt_group.update(screen,fps)
        design3.update(fps)
        if count1<1:
            count1+=1/fps
        else:
            design4.update(fps)
            design4.draw(screen)

        txt_group.draw(screen)
        design3.draw(screen)

    clock.tick(60)
    pg.display.flip()
pg.quit()
exit()


