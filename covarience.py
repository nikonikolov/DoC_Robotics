"""Module to calculate covarience matrix. Answer obtained is:

     [[ 0.59142618 -0.12348744]
      [-0.12348744  0.31164677]]
"""


import numpy as np

positions = [
    (-1.099656357,-0.06185567),
    (-1.257731959,0.261168385),
    (-1.271477663,0.611683849),
    (-1.828178694,1.237113402),
    (-1.443298969,0.783505155),
    (-1.642611684,2.096219931),
    (-1.085910653,0.728522337),
    (0.865979381,0.556701031),
    (-1.615120275,0.996563574),
    (-2.103092784,0.515463918),
]
xs = [p[0] for p in positions]
ys = [p[1] for p in positions]

mean_x = np.mean(xs)
mean_y = np.mean(ys)

var_x = sum((x - mean_x) * (x - mean_x) for x in xs) / len(positions)
var_y = sum((y - mean_y) * (y - mean_y) for y in ys) / len(positions)
var_x_y = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))  / len(positions)

print(np.array([[var_x, var_x_y],
                [var_x_y, var_y]]))
