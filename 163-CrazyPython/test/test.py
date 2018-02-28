# /usr/bin/env python
# -*- coding:utf-8 -*-
import math

# 自定义参数
baselen = 500
af_color_white="#FFFFFF"
af_color_red="#B22234"
af_color_blue="#3C3B6E"

# 国旗固定参数
af_stripe_length=1.9*baselen
af_stripe_width=0.0769*baselen

af_stararea_length=af_stripe_length*2/5
af_stararea_width=af_stripe_width*7

ad_star_high=af_stararea_width/10
af_star_drawlen=ad_star_high/math.cos(math.radians(18))
af_star_margin_left=(af_stararea_length-af_star_drawlen*11)/2
af_star_margin_top=ad_star_high-af_star_drawlen/2/math.cos(math.radians(18))*math.sin(math.radians(18))

print(ad_star_high)
print(af_star_drawlen)
print(af_star_margin_left)
print(af_star_margin_top)
print(af_star_drawlen/2/math.cos(math.radians(18))*math.sin(math.radians(18)))
