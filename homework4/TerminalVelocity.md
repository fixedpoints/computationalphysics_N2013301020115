###Terminal Velocity

If the velocity of an obeject obeys an equation of the form:  
<center></center>![][1]  
According to the solution ![][2], its velocity will approach a constant called terminal velocity.  
Here is an example.  
Let a = 10 and b = 1 and use python to calculate and plot the solution both numerially and exactly.  
The numerial method uses a 'for' cycle to simulate the Euler method to get the solution.  
The exact method uses 'odeint' function in scipy to get a relative exact solution of the ODE.  
Here is the figure of v(t).  
<center></center>![image](https://github.com/fixedpoints/computationalphysics_N2013301020115/blob/master/homework4/TerminalVelocity.png)  
Click [here](https://github.com/fixedpoints/computationalphysics_N2013301020115/edit/master/homework4/TerminalVelocity.py) to see the python source code.  

[1]: http://latex.codecogs.com/gif.latex?\\\frac{dv}{dt}=a-bv  
[2]: http://latex.codecogs.com/gif.latex?\v=a-e^{-bt}  
