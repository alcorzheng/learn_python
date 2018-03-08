# /usr/bin/env python
# -*- coding:utf-8 -*-
# 画美国国旗
import turtle
import math


# 自定义参数
baselen = 100
af_Color_White="#FFFFFF"
af_Color_Red="#B22234"
af_Color_Blue="#3C3B6E"

# 国旗固定参数
af_Stripe_Length=1.9*baselen
af_Stripe_Width=0.0769*baselen


af_StarArea_Width=af_Stripe_Width*7

ad_Star_High=af_StarArea_Width/10
af_Star_DrawLen=ad_Star_High/math.cos(math.radians(18))
af_Star_Margin_Left=0.0633*baselen/2
af_Star_Margin_Top=ad_Star_High-af_Star_DrawLen/2/math.cos(math.radians(18))*math.sin(math.radians(18))

af_StarArea_Length=af_Stripe_Length*2/5

def drawStripe(lineColor, fillColor):
    turtle.color(lineColor, fillColor)
    turtle.begin_fill()
    turtle.forward(af_Stripe_Length)
    turtle.right(90)
    turtle.forward(af_Stripe_Width )
    turtle.right(90)
    turtle.forward(af_Stripe_Length)
    turtle.right(90)
    turtle.forward(af_Stripe_Width)
    turtle.right(90)
    turtle.end_fill()
    return

def drawStar(lineColor, fillColor):
    turtle.color(lineColor, fillColor)
    turtle.begin_fill()
    for i in range(5):
        turtle.forward(af_Star_DrawLen)
        turtle.right(144)
    turtle.end_fill()
    return

def drawAllStripes(redColor,whiteColor):
    turtle.up()
    turtle.goto(0, 0)
    turtle.down()
    for i in range(13):
        turtle.up()
        turtle.goto(0, -af_Stripe_Width * i)
        turtle.down()
        drawColor = redColor if i%2==0 else whiteColor
        drawStripe(drawColor, drawColor)
    return

def drawStarArea(lineColor, fillColor):
    turtle.up()
    turtle.goto(0, 0)
    turtle.down()
    turtle.color(lineColor, fillColor)
    turtle.begin_fill()
    turtle.forward(af_StarArea_Length)
    turtle.right(90)
    turtle.forward(af_StarArea_Width)
    turtle.right(90)
    turtle.forward(af_StarArea_Length)
    turtle.right(90)
    turtle.forward(af_StarArea_Width)
    turtle.right(90)
    turtle.end_fill()
    return

def drawAllStars(starColor):
    turtle.up()
    turtle.goto(0, 0)
    turtle.down()
    for i in range(9):
        lineStarNum = 6 if i%2==0 else 5
        for j in range(lineStarNum):
            turtle.up()
            turtle.goto(af_Star_Margin_Left*(1+2*(i%2+2*j)),-af_Star_Margin_Top-ad_Star_High*i)
            turtle.down()
            drawStar(starColor, starColor)
    return

drawAllStripes(af_Color_Red,af_Color_White)
drawStarArea(af_Color_Blue,af_Color_Blue)
drawAllStars(af_Color_White)