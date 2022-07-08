# -*- coding: utf-8; -*-
#!/usr/bin/env python3

#########################################################
#              Author : Benjamin DE ZORDO               #
#########################################################
#                                                       #
#                     Description                       #
#   Take an picture in argument and save the Maxwell    #
#  spectrum as [spectrum_name_picture.png] in a folder  #
#                                                       #
#########################################################
#                                                       #
#                     Libxy Library                     #
#        Thanks for Y.Morel for this library            #
#  You can check it here : http://xymaths.free.fr/Libxy #
#                                                       #
#########################################################


# Import Libraries
import os, sys, math, numpy as np, matplotlib.pyplot as plt
from PIL import Image
from Libxy import *
#http://xymaths.free.fr/Informatique-Programmation/python/Libxy-download.php


""" 
Create a Maxwell triangle without colors:
Inspired by Frédéric Legrand : 
    https://www.f-legrand.fr/scidoc/docmml/image/niveaux/couleurs/couleurs.html
"""
def maxwell():
    a = 1.0/math.sqrt(3)
    plt.scatter([a,0,-a],[0,1,0],s=40,c=[(1,0,0),(0,1,0),(0,0,1)])
    #plt.figure(dpi=300)
    plt.plot([a,0,-a,a],[0,1,0,0],'k-')
    plt.axis([-0.7,0.7,-0.2,1.2])

""" 
@param  : rvb=[255,255,255]
Create a point :
    - "s" is the diameter
"""
def point(rvb):
    somme = int(rvb[0])+int(rvb[1])+int(rvb[2])
    if somme==0:
        somme=1
    r = (rvb[0]*1.0)/somme
    v = (rvb[1]*1.0)/somme
    b = (rvb[2]*1.0)/somme
    plt.scatter([(r-b)/math.sqrt(3)],[v],s=10,c=[(r,v,b)],marker = 'o')


"""
@param  : .jpg picture
"""
def main():
    arg=sys.argv[1]
    
    if((arg.split("."))[1]=="jpg"):
        image=arg
    else:
        print("Need a .jpg picture !")
        exit

    maxwell()
    imgpil = Image.open(image)
    pixels=imgpil.getcolors(maxcolors=3000000)

    list_pixel_already_view=[]
###############################################################
# In Process                                                  #
###############################################################
    for i in pixels[::10]:
        if(i not in list_pixel_already_view):
            list_pixel_already_view.append(i)
            point(i[1])
    #plt.show()
    name=os.path.basename(arg)
    plt.savefig(os.path.dirname(__file__)+ "\\SAVE\\spectrum_"+ name, dpi=1000)
    
main()

