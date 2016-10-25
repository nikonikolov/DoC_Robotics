import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


x = [
    138.5,
    138.5,
    161  ,
    158  ,
    159.5,
    177.5,
    114  ,
    112.5,
    90.5 ,
    91   ,
    69.5 ,
    70   ,
    45.5 ,
    46   ,
]
y = [
    6,
    6,
    7,
    7,
    7,
    8,
    5,
    5,
    4,
    4,
    3,
    3,
    2,
    2,
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
