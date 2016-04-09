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
def tr_shell(theta_d,dt,altitude=0,v=700):
    theta = theta_d/180.0 * math.pi
    x_shell_set, y_shell_set = [], []
    x_shell, y_shell = 0, 0
    v_shell = v
    t = 0
    g = -9.8
    cos_theta = math.cos(theta)
    sin_theta = math.sin(theta)
    v_shell_x = v_shell * cos_theta
    v_shell_y = v_shell * sin_theta
    while v_shell_x > 0:
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
        if y_shell < altitude and v_shell_y < 0:
            break
    x_shell_set.append(x_shell)
    y_shell_set.append(y_shell)
    return x_shell, t, x_shell_set, y_shell_set
    
#input a altitude
Altitude = input('please input an altitude within -4000 and 4000 \
to get the trajectory of maximum range.\n')
while Altitude < -4000 or Altitude > 4000:
    Altitude = input('please input an altitude within -4000 and 4000.\n')

#for a given altitude, calculate the best firing angle with time step = 0.01
def range_shell(theta_d,altitude=Altitude,v=700):
    return tr_shell(theta_d,0.01,altitude,v)[0]
    
range_set_1 = [range_shell(30+i,Altitude) for i in range(0,31)]
range_max_1 = max(range_set_1)
angle_max_1 = 30 + range_set_1.index(range_max_1)
angle_l = angle_max_1 - 2
angle_u = angle_max_1 + 2
range_set = [range_shell(angle_l+0.01*i,Altitude) for i in range(0,401)]
range_max = max(range_set)
angle_max = angle_l + 0.01*range_set.index(range_max)

#plot the trajectory in unit of kilometer under given altitude
import matplotlib.pyplot as plt
import numpy as np
tr_l_x = 0.001*np.array(tr_shell(angle_l,0.01,Altitude)[2])
tr_l_y = 0.001*np.array(tr_shell(angle_l,0.01,Altitude)[3])
tr_u_x = 0.001*np.array(tr_shell(angle_u,0.01,Altitude)[2])
tr_u_y = 0.001*np.array(tr_shell(angle_u,0.01,Altitude)[3])
tr_max_x = 0.001*np.array(tr_shell(angle_max,0.01,Altitude)[2])
tr_max_y = 0.001*np.array(tr_shell(angle_max,0.01,Altitude)[3])
plt.clf()
plt.plot(tr_l_x,tr_l_y,'g',label = '%.2f'%angle_l)
plt.plot(tr_u_x,tr_u_y,'b',label = '%.2f'%angle_u)
plt.plot(tr_max_x,tr_max_y,'r',label = '%.2f'%angle_max)
plt.xlabel('x/km')
plt.ylabel('y/km')
plt.ylim(ymin=min(Altitude,0))
plt.legend(loc=2)
ax = plt.subplot(111)
plt.text(0.5,0.3,'Altitude:%dm\nMax Range = %.1fm\nFiring Angle = %.2f degree'
        %(Altitude,range_max,angle_max),
        horizontalalignment='center',
        verticalalignment='center',
        transform=ax.transAxes)
plt.savefig('VariedMaxRange.png')


"""
for a given altitude and target (x,y), use the best firing angle to find 
the minimun firing velocity
"""
def min_velocity(x,y):
    v_test = round(1.0*x/range_max*700)
    while range_shell(angle_max,y,v_test) < x:
        v_test = v_test * 2
    v_test_0 = v_test
    pre = 1
    n = 1
    while abs(range_shell(angle_max,y,v_test)-x) >= 5:
        if range_shell(angle_max,y,v_test) < x:
            pre = pre + 1.0/(2**n)
            v_test = v_test_0 * pre
        else:
            pre = pre - 1.0/(2**n)
            v_test = v_test_0 * pre
        n += 1
    return v_test

#input a distance
Distance = input("please input a distance between shell and target \n\
to calculate the minimum velocity for your given distance \n\
and previous given altitude.\n\
the distance should be 0 to 100000.\n")
while Distance < 0 or Distance > 100000:
    Distance = input("please input a distance between shell and target.\n\
the distance should be 0 to 100000")

#get the minimum velocity under given distance and altitude
v_min = min_velocity(Distance,Altitude)
print 'v_min is %.2f when the target is (%d,%d)'%(v_min,Distance,Altitude)

plt.show()
