#suppose the initial velocity is 5, a = 10 and b = 1

#use Euler Method to calculate the numerial solution of v(t)
def v(t,dt):
    v = [5 for i in range(int(t/dt+1))]
    a = 10
    b = 1
    for i in range(int(t/dt)):
        v[i+1] = v[i] + (a-b*v[i])*dt
    return v

#set the time interval as 15s and the time step as 0.1s
v_n = v(15,0.1)
t_n = [0.1*i for i in range(151)]

#use scipy to calculate the exact solution of v(t)
from scipy.integrate import odeint
def dvdt(y,t):
    dvdt = 10 - y
    return dvdt
t_e = t_n
sol_v = odeint(dvdt,5,t_e)
v_e = sol_v[:,0]

#plot the solutions
import matplotlib.pyplot as plt
import numpy as np
plt.figure(figsize=(8,6))
plt.scatter(t_n,v_n,s=5,color='blue',label='numerial')
plt.plot(t_e,v_e,color='red',label='exact')
v_ter = [10 for i in range(151)]
plt.plot(t_e,v_ter,'--',color='green',label='TerminalVelocity')
plt.xticks(np.linspace(0,15,16,endpoint=True))
plt.yticks(np.linspace(5,12,8,endpoint=True))
plt.xlabel('t/s')
plt.ylabel('v/(m/s)')
plt.legend(loc='upper left',frameon=False)
plt.savefig('TerminalVelocity.png')
plt.show()
