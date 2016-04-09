"""
calcalute the acceleration caused by the air resistance.
tol means tolerance.
"""
import math
def a_air_resistance(v,y,tol=.0):
    B_2 = 0.00004
    y_0 = 1.0*10**4
    B_e = math.exp(-y/y_0) * B_2
    return -(1+tol)*B_e * v**2
    
"""
use numerial method to calculate the trajectory and range of cannon shell 
in different firing angle and time step
"""
def tr_shell(theta_d,dt,altitude=0,v=700,tol_air=.0):
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
        a_shell_y = a_air_resistance(v_shell,y_shell,tol_air) * sin_theta + g
        a_shell_x = a_air_resistance(v_shell,y_shell,tol_air) * cos_theta
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
    
#input the altitude of target
Altitude = input('please input an altitude within -4000 and 4000 \
as the altitude of the target.\n')
while Altitude < -4000 or Altitude > 4000:
    Altitude = input('please input an altitude wirthin -4000 and 4000.\n')
    
#input a distance
Distance = input("please input a distance between shell and target \n\
the distance should be 0 to 100000.\n")
while Distance < 0 or Distance > 100000:
    Distance = input("please input a distance between shell and target.\n\
the distance should be 0 to 100000")

#for a given altitude, calculate the best firing angle with time step = 0.01
def range_shell(theta_d,altitude=Altitude,v=700,tol_air=.0):
    return tr_shell(theta_d,0.01,altitude,v,tol_air)[0]
    
range_set_1 = [range_shell(30+i,Altitude) for i in range(0,31)]
range_max_1 = max(range_set_1)
angle_max_1 = 30 + range_set_1.index(range_max_1)
angle_l = angle_max_1 - 2
angle_u = angle_max_1 + 2
range_set = [range_shell(angle_l+0.01*i,Altitude) for i in range(0,401)]
range_max = max(range_set)
angle_max = angle_l + 0.01*range_set.index(range_max)



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

#get the minimum velocity under given distance and altitude
v_min = min_velocity(Distance,Altitude)
print 'Not taking tolerance into consideration, \n\
minimum velocity is %.2f with firing angle %.2f degree \n\
when the target is (%d,%d)'%(v_min,angle_max,Distance,Altitude)

#take tolerance into consider
def tol_range(theta,v,tol_theta,tol_v,tol_air):
    return range_shell((1+tol_theta)*theta,
                    Altitude,(1+tol_v)*v,tol_air) - Distance

#simulate random tolerance
import random
import numpy as np
def tol_range_tv(theta,v):
    rand = [0.001*random.randint(-10,10),
        0.005*random.randint(-10,10),
        0.01*random.randint(-10,10)]
    return tol_range(theta,v,rand[0],rand[1],rand[2]),rand

#calculate root-mean-square tolerance when sample size is 100
def tol_range_rms(theta,v):
    tols = []
    for i in range(100):
        tols.append(tol_range_tv(theta,v)[0])
    tols = np.array(tols)
    return np.sqrt(sum(tols**2))/50

#simulate the process randomly and give the minimum tolerance solution. 

rand_theta_set = []
rand_v_set = []
tol_set = []

import time
begin = time.time()
for i in range(100):
    rand_theta = angle_max + 0.01*random.randint(-200,200)
    rand_v = v_min * 0.01 *random.randint(90,110)
    tol_set.append(tol_range_rms(rand_theta,rand_v))
    rand_theta_set.append(rand_theta)
    rand_v_set.append(rand_v)
end = time.time()

tol_set.append(tol_range_rms(angle_max,v_min))
rand_theta_set.append(angle_max)
rand_v_set.append(v_min)

tol_min = min(tol_set)
index_mintol = tol_set.index(tol_min)
theta_mintol = rand_theta_set[index_mintol]
v_mintol = rand_v_set[index_mintol]

print 'Taking tolerance into consideration, \n\
firing velocity should be %.2f \n\
firing angle should be %.2f \n\
root-mean-square tolerance is %.5f.\n'%(v_mintol,theta_mintol,tol_min)

print '%d second was taken to simulate the effect \n\
caused by random tolerance in various velocity and firing angle.\n'%(end-begin)
