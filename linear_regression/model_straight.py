import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model


x = [
  21.35,
  21.75,
  24.5 ,
  24.5 ,
  27.1 ,
  27.1 ,
  32.8 ,
  32.9 ,
  38   ,
  38.2 ,
  46.7 ,
  46.2 ,
]
y = [
  8.0 ,
  8.0 ,
  9.0 ,
  9.0 ,
  10,
  10,
  12,
  12,
  14,
  14,
  17,
  17,
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


plt.xticks(np.arange(20, 50, .5))
plt.yticks(np.arange(0, 17, 1))
plt.grid()


a = lm.predict([[0], [5]])
m = (a[1] - a[0]) / (5.0)
c = lm.predict([[0]])[0]
print("m = ", m, "c=", c)

plt.show()
