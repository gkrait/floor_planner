from matplotlib import pyplot
from shapely.ops import split
import math 
from shapely.geometry import Polygon , LineString ,MultiPolygon
import numpy as np
from pprint import pprint  
import matplotlib.pyplot as plt
import random 
from copy import copy 
import matplotlib.patches as mpatches
import csv
plt.style.use('seaborn-whitegrid')

class Point:
	def __init__(self,x,y):
		self.x=x
		self.y=y

	def __repr__(self):
		return "("+str(self.x)+","+str(self.y)+")"
	def __add__(self,other):
		return Point(self.x+other.x , self.y+other.y)
	def __sub__(self,other):
		return Point(self.x-other.x , self.y-other.y)
	def __eq__(self, other):
		if isinstance(other, Point):
			return self.x == other.x and self.y == other.y
		return False
	def __mul__( self, other):
		if isinstance(other, int) or isinstance(other, float):
			self.x = self.x * other
			self.y = self.y * other
			return self	
	def __rmul__(self, other):
		return self * other	
	def dist(self,other):
	 return math.sqrt((self.x-other.x )**2+(self.y-other.y)**2  )		
        	
    

class Wall:
	def __init__(self,P1,P2, Label):
		self.P1=P1
		self.P2=P2
		self.Label=Label

	def __repr__(self):
		return  self.Label + ": [("+str(self.P1.x)+","+str(self.P1.y)+"),("+str(self.P2.x)+","+str(self.P2.y)+")]"
	def __eq__(self, other):
		if isinstance(other, Wall):
			return (self.P1 == other.P1 and self.P2 == other.P2) or (self.P2 == other.P1 and self.P1 == other.P2)
		return False
	
		
		
def add_extra(P1,P2,d,min_or_max="min"):
	if P1.x==P2.x:
		if min_or_max=="min":
			Pa=P1 +Point(-d,0)
			k=random.randint(P1.y+1,P2.y-1)
			#Pb=Pa+Point(0,(P1.y+P2.y)/k)
			Pb=Pa+Point(0,k)

		elif min_or_max=="max":
			Pa=P1 +Point(+d,0)
			k=random.randint(P1.y+1,P2.y-1)
			#Pb=Pa+Point(0,(P1.y+P2.y)/k)
			Pb=Pa+Point(0,k)
		
	elif P1.y==P2.y:
		if min_or_max=="min":
			Pa=P1 +Point(0,-d)
			k=random.randint(P1.x+1,P2.x-1)
			#Pb=Pa+Point((P1.x+P2.x)/k,0)
			Pb=Pa+Point(k,0)
		
			

		elif min_or_max=="max":
			Pa=P1 +Point(0,d)
			k=random.randint(P1.x+1,P2.x-1)
			Pb=Pa+Point((P1.x+P2.x)/k,0)
			Pb=Pa+Point(k,0)
	Pc= (P1-Pa)+Pb
	
	return [P1,P2,Pa,Pb,Pc]
	
def Plot_Wall(self):
		x_list=[self.P1.x,self.P2.x]
		y_list=[self.P1.y,self.P2.y]
		#plt.plot(x_list, y_list, 'o', color='black');
		if self.Label == "Exterior":
			plt.plot(x_list, y_list, color="black",label="Exterior",linewidth=5)
		elif self.Label == "Load_bearing":	
			plt.plot(x_list, y_list, color="brown",label="Load_bearing", linewidth=7)
		elif self.Label == "Plaster":	
			plt.plot(x_list, y_list, color="green",label="Plaster",linewidth=2)
		elif self.Label == "White":	
			plt.plot(x_list, y_list, color="White",label="White", linewidth=12)	

def Exterior_constructor(x1,x2,y1,y2,d):
		P00=Point(x1,y1)
		P01=Point(x1,y2)
		P10=Point(x2,y1)
		P11=Point(x2,y2)
		P0111=add_extra(P01,P11,d,"max")
		P0010=add_extra(P00,P10,d,"min")
		P0001=add_extra(P00,P01,d,"min")
		P1011=add_extra(P10,P11,d,"max")
		All_Points=[P0001,P0010,P1011,P0111] # est, north,  west,south
		Sides_type=[] 
		# Computing walls:
		All_Walls=[]
		for i in [1,2,3,0]:
			side_type=random.choice(["extra","normal"])
			Sides_type.append(side_type)
			if side_type =="normal":
				if  i in [1,2]:
				 W1=Wall(All_Points[i][0],All_Points[i][1],"Exterior")
				else:
					W1=Wall(All_Points[i][1],All_Points[i][0],"Exterior")
				All_Walls.append(W1)	

			elif side_type == "extra":
				if i in [1,2]:
					W2=Wall(All_Points[i][0],All_Points[i][2],"Exterior")
					W3=Wall(All_Points[i][2],All_Points[i][3],"Exterior")
					W4=Wall(All_Points[i][3],All_Points[i][4],"Exterior")
					W5=Wall(All_Points[i][4],All_Points[i][1],"Exterior")
				else:
			
					W2=Wall(All_Points[i][1],All_Points[i][4],"Exterior")
					W3=Wall(All_Points[i][4],All_Points[i][3],"Exterior")
					W4=Wall(All_Points[i][3],All_Points[i][2],"Exterior")
					W5=Wall(All_Points[i][2],All_Points[i][0],"Exterior")
				All_Walls = All_Walls + [W2,W3,W4,W5]	
					
		return [All_Walls,All_Points]	
				
				
		

def Find_max_Poly(Poly,checked_rooms=[]):
	k=0
	if type(Poly) == type(Polygon([(0,0),(0,1),(1,0)])):
		P_max=copy(Poly)
		x_min, y_min,x_max,y_max =Poly.bounds
		Max_len= [x_max-x_min,y_max-y_min]
		checked_rooms.append(Max_len)
	else:	
		Max_len =[0,0]
		i=0
		for P in list(Poly.geoms):
			x_min, y_min,x_max,y_max =P.bounds
			P_dims=[x_max -x_min ,y_max - y_min]
			if  max(Max_len) <= max(P_dims) and (P_dims not in checked_rooms):  #Max_area < P.area and P.area not in  checked_rooms:
				P_max=copy(P)
				Max_len = P_dims
				k=i
			i+=1	
		checked_rooms.append(Max_len)
	return [P_max,checked_rooms,k]

def split_rooms(Poly,n,min_len): 
	if n==1:
		return Poly
	num_polys=1
	checked_rooms=[]
	while num_polys <= n-1:
	 Maximal_Poly,checked_rooms,k = Find_max_Poly(Poly,checked_rooms)
	 x_min, y_min,x_max,y_max =Maximal_Poly.bounds
	 if (x_max - x_min) >= (y_max - y_min) :
	 	a=random.uniform(0.25*(x_min+x_max) ,0.75*(x_min+x_max))
	 	if min(x_max-a,a-x_min)< min_len :
	 		a=random.uniform(0.9,1.2)*0.5 *(x_max+x_min)
	 	L=LineString([(a, y_min), (a, y_max)])		
	 	
	 elif (x_max - x_min) < (y_max - y_min) :
	 	a=random.uniform(0.25*(y_min+y_max) ,0.75*(y_min+y_max))
	 	if min(y_max-a,a-y_min)< min_len :
	 		a= random.uniform(0.8,1.1)* 0.5 *(y_max+y_min)
	 	L=LineString([(x_min,a), (x_max,a)])
	 Grop1 = MultiPolygon(split(Maximal_Poly, L))
	 if  type(Poly) ==type(Grop1):
	 	Poly=MultiPolygon([[list(Poly[i].exterior.coords),[]] for i in range(len(Poly)) if i!=k]+[[list(P.exterior.coords),[]] for P in Grop1])
	 else:
	 	Poly=Grop1[:]

	 num_polys=len(Poly)
	return Poly 


def Plaster_gen(Exterior_Polygon,N,min_len):
 EX= ([ (W.P1.x,W.P1.y) for W in Exterior_Polygon] +[(W.P2.x,W.P2.y) for W in Exterior_Polygon])
 Poly=Polygon(EX).buffer(0)
 Poly=Poly.buffer(0)
 plan=split_rooms(Poly,N,min_len)
 Apartment=[list(P.exterior.coords) for P in plan ]
 Plaster_Walls=[]
 for P in plan:
	 Plaster_Walls.append([])
	 Room_points=list(P.exterior.coords)
	 Room=[]
	 for i in range(len(Room_points)-1):
		 W=Wall(Point(Room_points[i][0],Room_points[i][1]) ,\
			 Point(Room_points[i+1][0],Room_points[i+1][1]),"Plaster" )
		 if W not in EX  :
			 Room.append(W)

	 W=Wall(Point(Room_points[0][0],Room_points[0][1]) ,\
			 Point(Room_points[-1][0],Room_points[-1][1]) ,"Plaster" )
	 if W not in EX  :
			 Room.append(W)
	 Plaster_Walls.append(Room)
 return Plaster_Walls	 


def planner(x_min, y_min,x_max,y_max,N_rooms,d=1, min_len=1):
	Exterior_Walls, All_Points=Exterior_constructor(x_min,x_max,y_min,y_max,d)

	########################
	#Adding Load bearing (Randomly)
	##############################
	Load_bearing=[]
	for W in Exterior_Walls:
	  P=random.choice([W.P1,W.P2])
	  W_LB= Wall( P,  0.5*(W.P1+W.P2) , "Load_bearing")
	  Load_bearing.append(W_LB)
	########################
	#Adding Plaster (Randomly)
	##############################	  

	Plaster_Walls=Plaster_gen(Exterior_Walls,N_rooms,min_len)

	All_Walls=list(np.concatenate(Plaster_Walls).flat) + Exterior_Walls +Load_bearing
	return All_Walls
		
def Plot_Floor(Walls,x_min=0,y_min=0,x_max=7,y_max=12):
	plt.xlim([x_min-3, x_max+3])
	plt.ylim([y_min-3, y_max+3])
	Black_patch = mpatches.Patch(color="black", label='Exterior Walls')
	brown_patch = mpatches.Patch(color="brown", label='Load bearing')
	Green_patch = mpatches.Patch(color="green", label='Plaster Walls')
	plt.legend(handles=[Black_patch,brown_patch,Green_patch]) 

	for W in Walls:
		Plot_Wall(W)


	plt.show()	
  


def Mack_csv(Walls,fname="Walls"):
   
	List_dic=[]
	for W in Walls:
		Dic={"P1": W.P1, "P2":W.P2, "Label":W.Label  }
		List_dic.append(Dic)

	keys = List_dic[0].keys()
	with open(fname+".csv", 'w', newline='')  as output_file:
		dict_writer = csv.DictWriter(output_file, keys)
		dict_writer.writeheader()
		dict_writer.writerows(List_dic)	     
	return List_dic	







