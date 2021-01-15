from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import *

def draw_arrow(fx, fy, tx, ty, hs, fl):
  dx = tx - fx
  dy = ty - fy
  c = sqrt(dx * dx + dy * dy)

  angle = -degrees(asin(dy / c))

  sl = c - hs
  tl = fl * 2

  first_p = None
  second_p = None
  third_p = None
  fourth_p = None
  fith_p = None
  sixth_p = None
  seventh_p = None
  eighth_p = None
  
  if fx > tx:
    first_p = QPointF(fx, fy)
    second_p = QPointF(fx - fl * cos(radians(90 - angle)), fy + fl * sin(radians(90 - angle)))
    third_p = QPointF(second_p.x() - sl * cos(radians(angle)), second_p.y() - sl * sin(radians(angle)))
    fourth_p = QPointF(third_p.x() - tl * cos(radians(90 - angle)), third_p.y() + tl * sin(radians(90 - angle)))
    fith_p = QPointF(tx, ty)
    sixth_p = QPointF(third_p.x() + (tl * 2) * cos(radians(90 - angle)), third_p.y() - (tl * 2) * sin(radians(90 - angle)))
    seventh_p = QPointF(sixth_p.x() - tl * cos(radians(90 - angle)), sixth_p.y() + tl * sin(radians(90 -angle)))
    eighth_p = QPointF(seventh_p.x() + sl * cos(radians(angle)), seventh_p.y() + sl * sin(radians(angle))) 
  else:
    first_p = QPointF(fx, fy)
    second_p = QPointF(fx - fl * cos(radians(90 - angle)), fy - fl * sin(radians(90 - angle)))
    third_p = QPointF(second_p.x() + sl * cos(radians(angle)), second_p.y() - sl * sin(radians(angle)))
    fourth_p = QPointF(third_p.x() - tl * cos(radians(90 - angle)), third_p.y() - tl * sin(radians(90 - angle)))
    fith_p = QPointF(tx, ty)
    sixth_p = QPointF(third_p.x() + (tl * 2) * cos(radians(90 - angle)), third_p.y() + (tl * 2) * sin(radians(90 - angle)))
    seventh_p = QPointF(sixth_p.x() - tl * cos(radians(90 - angle)), sixth_p.y() - tl * sin(radians(90 -angle)))
    eighth_p = QPointF(seventh_p.x() - sl * cos(radians(angle)), seventh_p.y() + sl * sin(radians(angle)))

  poly = QPolygonF()
  poly.append(first_p)
  poly.append(second_p)
  poly.append(third_p)
  poly.append(fourth_p)
  poly.append(fith_p)
  poly.append(sixth_p)
  poly.append(seventh_p)
  poly.append(eighth_p)
  return poly