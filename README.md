# Autumatic Floor Planner

This is a brief explaination of  a  prototype that revisis  Autumatic Floor Planner problem.

The main motivation is to generate training data for related machine learning problems. The goal of this prototype is to have an example in
hand to discuss, determine and understand the main goal more precisely. Let us start with how the implementation works:

## Algorithm

In fact, I chose a subdivision strategy, since it is as general as we want and more understandable as a start. 

1.   Generate a list rectangle of "proper" width and length desired.
2.   choose a "proper" ration to divide over the length or width. Now we have a list of two polygons.
3. Choose a polygon with a maximal width or length and apply Step(2) again.
4. repeat until all Room numbers conditions are satisfied. 

I tried my best in the code to make it as flexible as possible for accepting future improvements.

## Python Module
The module *floor_planner* consists of 3 main functions: *planner, Plot_Floor* and *Mack_csv*.  
 To use it locally, please make sure to install: *matplotlib, shapely, numpy* and *csv*. If you find any problem in using it. Please do not hesitate to contact me. 
##*planner(x_min, y_min,x_max,y_max,N_rooms,d=0.5, min_len=1)*  Function

I am aware that the expected entries are  max-min areas & max-min number of rooms. However, for practical reasons, I chose to slightly change the input type to avoid technical bugs.  
The input of the this function are  *x_min, y_min,x_max,y_max* that represent the boundaries of appartment. the variable *d*  represents the error allowed, that is, the width of the floor is between \\
[x_min-d,x_max+d] and so  is the length [y_min-d,y_max+d].
Simply, the variable *N_rooms* represents the number of rooms. 

The output is a randomly-generated list of objects of type Wall. Each object has three attributes: P1, P2 and label. P1, P2 are 2D-points with float entries. Label is a string that is in the set:

{"Exterior", "Load bearing","Plaster"}.
The shape of the exterior polygon is almost a rectangular except additional smaller rectangles that are randomly added to some sides of the bigger rectangular.




### Example


```Python
#Computing the Walls 
import floor_planner as fp 
from pprint import pprint
All_Walls=fp.planner(0,0,15,10,7,3, 4)
pprint(All_Walls[:3]) # The first 3 elements of All_Walls
```
### The results
```
[Plaster: [(0.0,4.806029753560055),(0.0,10.0)],
 Plaster: [(0.0,10.0),(6.535776882798447,10.0)],
 Plaster: [(6.535776882798447,10.0),(6.535776882798447,4.806029753560055)]]
```
## Ploting the Walls
```Python
fp.Plot_Floor(All_Walls,x_min=-4, x_max=25)
```

```
[<img src="https://colab.research.google.com/drive/17xVpGMrv9zDc2BO_s9ojL2nwcD3EpJb6#scrollTo=h4Mv8AZeBOHT&line=1&uniqifier=1">](https://colab.research.google.com/drive/17xVpGMrv9zDc2BO_s9ojL2nwcD3EpJb6#scrollTo=h4Mv8AZeBOHT&line=1&uniqifier=1)

```
