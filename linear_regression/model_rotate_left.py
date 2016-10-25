import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


x = [
    45   ,
    45   ,
    68   ,
    69   ,
    90   ,
    89.5 ,
    114.5,
    114  ,
    136  ,
    138  ,
    159.5,
    158,
]
y = [
    2,
    2,
    3,
    3,
    4,
    4,
    5,
    5,
    6,
    6,
    7,
    7,
]
x_input = [[row] for row in x]

lm = linear_model.LinearRegression()
lm.fit(x_input , y)
print(lm)
print(lm.coef_)
print(lm.get_params())

plt.scatter(x, y,  color='black')
plt.plot(x, lm.predict(x_input), color='blue',
         linewidth=3)


plt.xticks(np.arange(0, 180, 5))
plt.yticks(np.arange(0, 11, 1))
plt.grid()


a = lm.predict([[0], [5]])
m = (a[1] - a[0]) / (5.0)
c = lm.predict([[0]])[0]
print("m = ", m, "c=", c)

plt.show()
