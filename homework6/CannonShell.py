"""
calcalute the acceleration caused by the air resistance 
"""
import math
def a_air_resistance(v,y):
    B_2 = 0.00004
    y_0 = 1.0*10**4
    B_e = math.exp(-y/y_0) * B_2
    return -B_e * v**2

"""
use numerial method to calculate the trajectory and range of cannon shell 
in different firing angle and time step
"""
def tr_shell(theta_d,dt):
    theta = theta_d/180.0 * math.pi
    x_shell_set, y_shell_set = [], []
    x_shell, y_shell = 0, 0
    v_shell = 700
    t = 0
    g = -9.8
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    v_shell_x = v_shell * cos_theta
    v_shell_y = v_shell * sin_theta
    while y_shell >= 0:
        x_shell_set.append(x_shell)
        y_shell_set.append(y_shell)
        a_shell_y = a_air_resistance(v_shell,y_shell) * sin_theta + g
        a_shell_x = a_air_resistance(v_shell,y_shell) * cos_theta
        x_shell = x_shell + v_shell_x * dt
        y_shell = y_shell + v_shell_y * dt
        v_shell_x = v_shell_x + a_shell_x * dt
        v_shell_y = v_shell_y + a_shell_y * dt
        v_shell = math.sqrt(v_shell_x**2 + v_shell_y**2)
        sin_theta = v_shell_y/v_shell
        cos_theta = v_shell_x/v_shell
        t += dt
    x_shell_set.append(x_shell)
    y_shell_set.append(y_shell)
    return x_shell, t, x_shell_set, y_shell_set

#get the range of cannon shell with time step as 0.01 second in different angle
def range_shell(x):
    return tr_shell(x,0.01)[0]

"""
search the maximum range of cannon shell with firing angle in [45,50]
under presision of 0.01 degree
"""
range_set = [range_shell(45+0.01*i) for i in range(501)]
range_max = max(range_set)
angle_max = 45 + 0.01*range_set.index(range_max)

#plot the trajectory in unit of kilometer
import matplotlib.pyplot as plt
import numpy as np
tr_45_x = 0.001*np.array(tr_shell(45,0.01)[2])
tr_45_y = 0.001*np.array(tr_shell(45,0.01)[3])
tr_50_x = 0.001*np.array(tr_shell(50,0.01)[2])
tr_50_y = 0.001*np.array(tr_shell(50,0.01)[3])
tr_max_x = 0.001*np.array(tr_shell(angle_max,0.01)[2])
tr_max_y = 0.001*np.array(tr_shell(angle_max,0.01)[3])
plt.clf()
plt.plot(tr_45_x,tr_45_y,'g',label = '45.00')
plt.plot(tr_50_x,tr_50_y,'b',label = '50.00')
plt.plot(tr_max_x,tr_max_y,'r',label = '%.2f'%angle_max)
plt.xlabel('x/km')
plt.ylabel('y/km')
plt.ylim(ymin=0)
plt.legend(loc=2)
ax = plt.subplot(111)
plt.text(0.5,0.3,'Max Range = %.1fm\nFiring Angle = %.2f degree'%(range_max,angle_max),
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes)
plt.savefig('MaxRange.png')
plt.show()

