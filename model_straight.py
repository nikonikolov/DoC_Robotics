import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model

x = [
    5 ,
    6 ,
    7 ,
    8 ,
    9 ,
    10,
    5 ,
    6 ,
    7 ,
    8 ,
    9 ,
    10,
]
x_input = [[row] for row in x]

y = [
17.2 ,
20.55,
23.6 ,
27   ,
30.65,
34   ,
17   ,
20.35,
23.6 ,
27.05,
30.45,
33.99,
]

lm = linear_model.LinearRegression()
lm.fit(x_input , y)
print(lm)
print(lm.coef_)
print(lm.get_params())

plt.scatter(x, y,  color='black')
plt.plot(x, lm.predict(x_input), color='blue',
         linewidth=3)


plt.xticks(np.arange(0, 11, 1))
plt.yticks(np.arange(17, 35, .5))
plt.grid()


a = lm.predict([[0], [5]])
m = (a[1] - a[0]) / (5.0)
c = lm.predict([[0]])[0]
print("m = ", m, "c=", c)

plt.show()
