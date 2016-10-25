import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


x = [
    174,
    153.5,
    133  ,
    103  ,
    73.5 ,
    48.5 ,
    22   ,
    37.5 ,
    63.5 ,
    93   ,
    116  ,
    144  ,
    171  ,
]
y = [
    7  ,
    6  ,
    5  ,
    4  ,
    3  ,
    2  ,
    1  ,
    1.5,
    2.5,
    3.5,
    4.5,
    5.5,
    6.5,
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
