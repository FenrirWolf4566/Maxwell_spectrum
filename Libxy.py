# -*- coding: utf-8; -*-
################################################################################

"""
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:

 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
__version__="2.1"
__author__="Y. Morel"
__about__="Library for graphical functions and tools with pure python - written by "+__author__+", detailled infos on http://xymaths.free.fr/Libxy "
__date__="2017"

import platform, sys, os.path
r=platform.python_version()
if (int(r[0])==2): pyv=2;print("Using Libxy"+__version__+" withpython 2.x\n")
elif (int(r[0])==3): pyv=3;print("Using Libxy",__version__," with python 3.x\n")
else: pyv=3;print("Using Libxy ",__version__," with undefined version of python is used, assuming 3.x\n")

def InitGraph (Xmin=-10,Xmax=10,Ymin=-10,Ymax=10,**kwargs):
    global Width, Height
    global xmin, xmax, ymin, ymax
    global ptsz, lw, lc
    global palette, bitarray
    ptsz=kwargs.get('PointSize',1)
    lw=kwargs.get('LineWidth',1)
    lc=kwargs.get ('LineColor',"blue")
    #Width=int(kwargs.get('Width',500))
    #Height=int(kwargs.get('Height',500))
    Size=int(kwargs.get('Size',400))
    # Image carrée pour l'instant
    Width=Size;Height=Size;#Width=400;Height=400 
    bkgd=kwargs.get('background',"white")
    tmparray = [ 0 ] * Height
    bitarray = [ tmparray[:] for i in range( Width ) ]
    xmin,xmax,ymin,ymax=float(Xmin),float(Xmax),float(Ymin),float(Ymax)

    bkgdrgb=RGBColorByName(bkgd) # background color
    palette = []
    #palette.append( hash(bkgdrgb) )

    palette.append(hash(RGBColorByName("white")))
    palette.append(hash(RGBColorByName("black")))
    global blackplidx
    blackplidx=palette.index(hash(RGBColorByName("black")))
    #print("black index pl= ",blackplidx) 
    palette.append(hash(RGBColorByName("blue")))
    palette.append(hash(RGBColorByName("red")))
    palette.append(hash(RGBColorByName("green")))
    palette.append(hash(RGBColorByName("cyan")))
    palette.append(hash(RGBColorByName("magenta")))
    palette.append(hash(RGBColorByName("yellow")))
    palette.append(hash(RGBColorByName("purple")))
    palette.append(hash(RGBColorByName("gray")))
    palette.append(hash(RGBColorByName("brown")))
    #print("palette=",palette)



def shortToString(i):
  hi = (i & 0xff00) >> 8
  lo = i & 0x00ff
  if pyv==2:
      return chr(lo) + chr(hi)
  elif pyv==3:
      return bytes([lo]) + bytes([hi])

def longToString(i):
  hi = (int(i) & 0x7fff0000) >> 16
  lo = int(i) & 0x0000ffff
  return shortToString(lo) + shortToString(hi)

def long24ToString(i):
  if pyv==2:
      return chr(i & 0xff) + chr(i >> 8 & 0xff) + chr(i >> 16 & 0xff)
  elif pyv==3:
      #return bytes([i & 0xff]) + bytes([i >> 8 & 0xff]) + bytes([i >> 16 & 0xff])
      return bytes([i >> 16 & 0xff]) + bytes([i >> 8 & 0xff]) + bytes([i & 0xff])


def stringToLong(input_string, offset):
  return ord(input_string[offset+3]) << 24 | ord(input_string[offset+2]) << 16 | ord(input_string[offset+1]) << 8 | ord(input_string[offset])

def stringToLong24(input_string, offset):
  return ord(input_string[offset+2]) << 16 | ord(input_string[offset+1]) << 8 | ord(input_string[offset])

def hash(color): #color=(r,g,b)
    return ( ( int(color[0]) ) + 
             ( int(color[1]) <<  8 ) + 
             ( int(color[2]) << 16 ) )

def RGBColorByName(color):
    if color=="black" or color=="k":
        rgb=(   0,   0,   0 )
    elif color=="white" or color=="w":
        rgb=( 255,   255,   255 )
    elif color=="red" or color=="r":
        rgb=( 255,   0,   0 )
    elif color=="green" or color=="g":
        rgb=(   0, 255,   0 )
    elif color=="blue" or color=="b":
        rgb=(   0, 0,   255 )
    elif color=="indigo" or color=="i":
        rgb=(   75, 0,   130 )
    elif color=="orange" or color=="orange":
        rgb=(   255, 165,  0)
    elif color=="cyan":
        rgb=(   0, 255,   255 )
    elif color=="magenta" or color=="m":
        rgb=( 255,   0, 255 )
    elif color=="yellow" or color=="y":
        rgb=( 255, 255,   0 )
    elif color=="teal":
        rgb=(   0, 128, 128 )
    elif color=="purple" or color=="p":
        rgb=( 128,   0, 128 )
    elif color=="brown":
        rgb=( 150, 75,   0)
    elif color=="chocolate" or color=="c":
        rgb=( 210, 105,   30)
    elif color=="gray":
        rgb=( 128, 128, 128 )
    elif color=="pink":
        rgb=( 255, 20, 147 )
    elif color=="darkred":
        rgb=( 128,   0,   0 )
    elif color=="darkgreen":
        rgb=(   0, 128,   0 )
    elif color=="darkblue":
        rgb=(   0,   0, 128 )
    else:
        print("Unknown color: "+color)
        print("using defaut: black color")
        rgb=(   0,   0,   0 )        
    return rgb


def MakePalette( color ):
    if not(isinstance(color,str)):
        # If color is given via rgb=(r,g,b)
        n=len(color)
        if (n==3):
            rgbcolornum=hash(color)
        else:
            print("Color must either be called with a valid color name (e.g. black, blue, red, green, ...) or  be an array of RGB colors, with 3 parameters color=(r,g,b) where 0<=r,g,b<=256\nUsing black color instead...")
            rgbcolornum=hash(RGBColorByName("black"))
    else: 
        rgbcolor=RGBColorByName(color)
        rgbcolornum=hash(rgbcolor)

    try:
        plidx=palette.index( rgbcolornum )
    except ValueError:
        if len(palette) < 256 :
            palette.append( rgbcolornum )
            plidx=len(palette)-1
        else:
            plidx = blackplidx
    return plidx

def coord (X,Y):
    x=xmin+X*(xmax-xmin)*1.0/Width
    y=ymin+Y*(ymax-ymin)*1.0/Height
    #print("coord  |",Width,X,x)
    return x, y

def coordim (x,y):
    X=Width*(x-xmin)*1.0/(xmax-xmin)
    Y=Height*(y-ymin)*1.0/(ymax-ymin)
    return X, Y

def Point (*args,**kwargs):
    sz1=kwargs.get ('size',False)
    sz2=kwargs.get ('PointSize',False)
    if sz2: 
        sz=sz2
    elif sz1:
        sz=sz1
    else:
        sz=ptsz
    fill=kwargs.get ('fill',"red")
    if (len (args)==1):
        try: 
            A=(args [0][0],args [0][1])
        except TypeError:
            print("Trying to execute: Point"+str(args))
            print("Two coordinates are required to define a point")
            print(" Point(x,y)  or A=(x,y);Point(A)\n")
            exit()
    elif (len (args)==2):
        try: 
            tmp=len(args[0])
            A=(args [0][0],args [0][1])
            try:
                sz=int(args[1])
            except ValueError:
                fill=args[1]
        except TypeError: 
            A=(args[0],args[1])
    elif (len(args)==3):
        try: 
            tmp=len(args[0])
            A=(args [0][0],args [0][1])
            try:
                sz=int(args[1])
                fill=args[2]
            except ValueError:
                sz=args[2]
                fill=args[1]
        except TypeError:
            A=(args[0],args[1])
            try:
                sz=int(args[2])
            except ValueError:
                fill=args[2]
    elif (len(args)==4):
        A=(args[0],args[1])
        try:
            sz=int(args[2])
            fill=args[3]
        except ValueError:
            try:
                sz=int(args[3])
            except ValueError:
                print("Bad syntax used in Point(),", args[3]," not recognized")
            fill=args[2]
    plidx=MakePalette(fill)
    [X,Y]=coordim(A[0],A[1])
    X=int(X);Y=int(Y)
    if sz<=1:
        if ( 0 <= X < Width and 0 <= Y < Height ):
            bitarray[X][Y] = plidx
    else:
        bz=int(sz/2.0)
        if ( bz <= X < Width-bz and bz <= Y < Height-bz ):
            for i in range (-bz,bz):
                for j in range (-bz,bz):
                    bitarray[X+i][Y+j] = plidx

def Points (*args,**kwargs):
    fill=kwargs.get ('fill',"red")
    sz=int (kwargs.get ('size',ptsz))
    for i in range (len (args)):
        Point (args[i],size=sz,fill=fill)

def Line (A,B,**kwargs):
    fill=kwargs.get ('fill',lc)
    width=kwargs.get ('width',lw)
    xA=A[0];yA=A[1];xB=B[0];yB=B[1]
    if not(xB==xA):
        m=(yB-yA)*1.0/(xB-xA)
        if m<0.5:
            p=yA-m*xA
            for i in range(Width):
                xi=xA+i*1.0*(xB-xA)/Width;
                yi=m*xi+p
                #print(xi,yi,coordim(xi,yi))
                Point(xi,yi,size=width,fill=fill)
        else:
            m=(xB-xA)*1.0/(yB-yA)
            p=xA-m*yA
            for i in range(Height):
                yi=yA+i*1.0*(yB-yA)/Height;
                xi=m*yi+p
                Point(xi,yi,size=width,fill=fill)
    else: #if xB==xA
        for i in range(Height):
            yi=yA+i*1.0*(yB-yA)/Height;
            xi=xA
            Point(xi,yi,size=width,fill=fill)
        
def Lines (*args,**kwargs):
    fill=kwargs.get ('fill',lc)
    width=kwargs.get ('width',lw)
    for i in range (len (args)-1):
        Line (args[i],args[i+1],fill=fill,width=width)


def Polygon (*args,**kwargs):
    outline=kwargs.get ('outline',lc)
    fill=kwargs.get ('fill',None)
    width=kwargs.get ('width',lw)
    N=len (args)

    if (fill): 
        # Polygon's bounding box 
        tmparray = [ 0 ] * N
        for i in range(N): tmparray[i]=args[i][0]
        xpolmin=min(tmparray);xpolmax=max(tmparray)
        for i in range(N): tmparray[i]=args[i][1]
        ypolmin=min(tmparray);ypolmax=max(tmparray)
        M1=(xpolmin,ypolmin);
        M2=(xpolmax,ypolmin)
        M3=(xpolmax,ypolmax)
        M4=(xpolmin,ypolmax)
        #Lines(M1,M2,M3,M4,M1)
        #print("filling polygon in",fill)
        (Xpolmin,Ypolmin)=coordim(xpolmin,ypolmin)
        (Xpolmax,Ypolmax)=coordim(xpolmax,ypolmax)
        prec=.75*(xmax-xmin)/Width
        I=[0,0]
        for xx in range(int(Xpolmin),int(Xpolmax)):
            R=(xx,int(Ypolmax)+2);
            R=coord(*R);
            for yy in range(int(Ypolmin),int(Ypolmax)):
                M=coord(xx,yy)
                cpt=0;Vrt=0;brd=0
                for i in range(N): 
                    A=args[i];
                    if (i<N-1): B=args[i+1]
                    else: B=args[0]
                    # (RM): x=xx
                    if not(B[0]==A[0]): # then (RM) intersects (AB) in I
                        # (AB): y=mx+p
                        m=(B[1]-A[1])*1.0/(B[0]-A[0])
                        p=A[1]-m*A[0]
                        I[0]=R[0]
                        I[1]=m*R[0]+p
                        if (Norm(A,I)<prec or (Norm(B,I)<prec)): Vrt=1
                        if (Norm(M,I)<2.5*prec): brd=1
                    if ((I[0]-A[0])*(I[0]-B[0])<0 and (I[1]-R[1])*(I[1]-M[1])<0):
                        cpt+=1
                if (cpt%2) and not(Vrt) and not(brd): Point(M,size=4,fill=fill)
    if width>=1:
        for i in range (N-1):
            Line (args[i],args [i+1],width=width,fill=outline)
        Line (args [N-1],args [0],width=width,fill=outline)

def Norm (A,B):
    return ((B[0]-A[0])**2+(B[1]-A[1])**2)**0.5

def Axes (xtick=0,ytick=0):
    if xtick<=0: xtick=(xmax-xmin)/10
    for i in range(int (xmin/xtick),int(xmax/xtick)+1):
        x=i*xtick
        y=(ymax-ymin)/200
        Line ((x,y), (x,-y),fill="blue")
        istr=str(int(i*xtick*100)/100.0)
        #Text ((x,-2*y),istr,fill="blue")
    if ytick<=0: ytick= (ymax-ymin)/10
    for i in range(int (ymin/ytick),int(ymax/ytick)+1):
        y=i*ytick
        x=(xmax-xmin)/200
        Line ((x,y), (-x,y),fill="blue")
        istr=str(int(i*ytick*100)/100.0)
        #Text ((-4*x,y),istr,fill="blue")
    Line ((xmin,0), (xmax,0),fill="blue",width=2)
    Line ((0,ymin), (0,ymax),fill="blue",width=2)
    global XtickAxes, YtickAxes
    XtickAxes,YtickAxes=xtick,ytick

def Grid (Dx=0,Dy=0):
    if not Dx>0:
        try:
            Dx=XtickAxes
        except NameError:
            Dx=(xmax-xmin)/10
    if not Dy>0:
        try:
            Dy=YtickAxes
        except NameError:
            Dy=(ymax-ymin)/10 
    for i in range(int (xmin/Dx),int(xmax/Dx)+1):
        x=i*Dx
        for j in range (0,100):
            y=ymin+j*(ymax-ymin)/100
            Point ((x,y),size=1,fill="orange")
    for i in range(int (ymin/Dy),int(ymax/Dy)+1):
        y=i*Dy
        for j in range (0,100):
            x=xmin+j*(xmax-xmin)/100
            Point ((x,y),size=1,fill="orange")


def Circle (*args,**kwargs):
    R=kwargs.get('R',False)
    outline=kwargs.get ('outline',lc)
    fill=kwargs.get ('fill',None)
    width=kwargs.get ('width',lw)
    N=len (args)
    if len(args)==1 and not(R):
        print("R is missing for circle, using R=0 (plotting a single point)")
        O=(args [0][0],args [0][1])
    elif len(args)==2 and not(R):
        O=(args[0][0],args[0][1])
        R=args[1]
    elif len(args)==2 and not(R):
        O=(args [0][0],args [0][1])
        R=args[1]
    elif len(args)==3 and not(R):
        O=(args[0],args[1])
        R=args[2]
    elif len(args)==3 and R:
        O=(args[0],args[1])
        
    N=min([4*int(1.0*Width*R/max([xmax-xmin,ymax-ymin])),2*Width])
    if R>0:
        if (fill):
            for i in range(N):
                if i<N/4:
                    x=O[0]-R+2.0*i**2*R/N**2
                elif i<3*N/4: 
                    x=O[0]-R+2.0*(i-N/4)*R/(N/2)
                else:
                    x=O[0]+R-2.0*(N-i)**2*R/N**2
                y1=O[1]+(R**2-(x-O[0])**2)**0.5
                y2=O[1]-(R**2-(x-O[0])**2)**0.5
                for j in range(N):
                    Point(x,y1+j*(y2-y1)*1.0/N,size=width,fill=fill)
            Circle(O,R,width=width,outline=outline)    
        else:
            for i in range(N):
                if i<N/4:
                    x=O[0]-R+2.0*i**2*R/N**2
                elif i<3*N/4: 
                    x=O[0]-R+2.0*(i-N/4)*R/(N/2)
                else:
                    x=O[0]+R-2.0*(N-i)**2*R/N**2
                y1=O[1]+(R**2-(x-O[0])**2)**0.5
                y2=O[1]-(R**2-(x-O[0])**2)**0.5
                Point(x,y1,size=width,fill=outline)
                Point(x,y2,size=width,fill=outline)
    else:
        Point(A,fill=outline,size=width)
    
def Norm (A,B):
    return ((B[0]-A[0])**2+(B[1]-A[1])**2)**0.5

def Vector (A,B,fill="red",width=1,ArrowLength=0.5,ArrowWidth=0.3):
    #"cf. http://xymaths.free.fr/Informatique-Programmation/javascript/canvas-dessin-fleche.php"
    AB=Norm(A,B)
    xA=A[0];yA=A[1]
    xB=B[0];yB=B[1]
    xC=xB+ArrowLength*(xA-xB)/AB
    yC=yB+ArrowLength*(yA-yB)/AB
    xD=xC+ArrowWidth*(-(yB-yA))/AB
    yD=yC+ArrowWidth*((xB-xA))/AB
    xE=xC-ArrowWidth*(-(yB-yA))/AB
    yE=yC-ArrowWidth*((xB-xA))/AB
    Line (A,B,fill=fill,width=width)
    D=(xD,yD);E=(xE,yE)
    Lines (D,B,E,fill=fill,width=width)

def SaveGraph (filename="Picture"):

#def WriteBMP(filename,width,height):
    #wd = Width #int(width)
    #ht = Height #int(height) 

    #f = file( filename, "wb" )
    path=os.path.abspath(os.path.dirname(__file__))
    fullPicName=path+'/'+filename+'.bmp'
    #f = open( filename, "wb" )
    f = open( fullPicName , "wb" )
    
    line_padding = (4 - (Width % 4)) % 4
    
    # write bitmap header
    if pyv==2: 
        f.write("BM")
        #f.write( longToString( 54 + 256*4 + self.ht*self.wd ) )   # DWORD size in bytes of the file
    elif pyv==3: 
        f.write(bytes("BM",'ascii'))
        
    f.write( longToString( 54 + Height*(Width*3 + line_padding) ) )   # DWORD size in bytes of the file
    f.write( longToString( 0 ) )    # DWORD 0
    #f.write( longToString( 54 + 256*4 ) )    # DWORD offset to the data
    f.write( longToString( 54  ) )
    f.write( longToString( 40 ) )    # DWORD header size = 40
    f.write( longToString( Width ) )    # DWORD image width
    f.write( longToString( Height ) )    # DWORD image height
    f.write( shortToString( 1 ) )    # WORD planes = 1
    f.write( shortToString( 24 ) )    # WORD bits per pixel = 8
    f.write( longToString( 0 ) )    # DWORD compression = 0
    f.write( longToString( Height * (Width * 3 + line_padding) ) )    # DWORD sizeimage = size in bytes of the bitmap = width * height
    f.write( longToString( 0 ) )    # DWORD horiz pixels per meter (?)
    f.write( longToString( 0 ) )    # DWORD ver pixels per meter (?)
    f.write( longToString( 0 ) )    # DWORD number of colors used = 256
    f.write( longToString( 0 ) )    # DWORD number of "import colors = len( self.palette )

    # write pixels
    #bitarray.reverse()
    #for row in bitarray:
    #    for pixel in row:
    for X in range(Width):
        for Y in range(Height):
            c = palette[bitarray[Y][X]]
            f.write( long24ToString(c) )
        for i in range(line_padding):
            if pyv==2: 
                f.write( chr( 0 ))
            elif pyv==3:
                f.write( bytes([0]))
    
    # close file
    f.close()
    print("\nImage "+filename+".bmp saved in "+path+"\n")

if __name__ == '__main__':
    print("\nLibxy, version : "
    	  +str (__version__))

"""
Usage: 
form Libxy import *
InitGraph()
#
#Graphical and python programming instructions 
#
SaveGraph()

See xymaths.free.fr/Libxy for detailled informations
"""
