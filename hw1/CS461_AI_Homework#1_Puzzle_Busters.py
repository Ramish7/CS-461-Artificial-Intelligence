#Homewor1 AI 

'''
Part a 


Firstly we will represent a state as a tuple (x,y) where x represents the amount of water 
in the 10-liter jug and y represents the amount of water in the 6-liter jug. Also, we will
use the following notations for the jugs : 'A' for the 10-liter jug and 'B' for the 6-liter 
jug.
 

1) What are the states ?  
-There are (7*11) possible states but only 16 are allowed in our case. In fact, some states
are not authorized due to the constraints when using the operators (fill A, dump B ...)

-The 16 states are : 
(0,0) (10,0)  (0,6)  (6,0)  (6,6)  (10,2) (0,2) (2,0)  (2,6)  (8,0)  (8,6)  (10,4)     
(0,4)  (4,0)  (4,6)  (10,6) 


2) What are the initial and goal states ? 
-Initial state : (0,0)
-Goal state : (8,y)    

3) What are the operators ? 
-Fill A : (x,y) <-- (10,y), x<10 
-Fill B : (x,y) <-- (x,6), y<10 
-Dump A : (x,y) <-- (0,y), x>0 
-Dump A : (x,y) <-- (x,0), y>0     
-Pour A to B : {if (x<=(6-y)) then x=0 and y=y+x 
                if (x>(6-y)) then x=x-(6-y) and y=6}
-Pour B to A : {if (y<=(10-x)) then x=x+y and y=0 
                if (y>(10-x)) then x=10 and y=y-(10-x)}

4) What is the branching factor ? 
-The branching factor is the number of the children at each node. If the value is not 
uniform an average branching factor can be calculated.  
-The average branching factor is : 58/16 = 3.625     


'''

from random import randint

capacity = (10,6)
# Maximum capacities of 2 jugs -> x,y
x = capacity[0]
y = capacity[1]

# to mark visited states
memory = {}

# store solution path
ans = []

def get_all_states(state):
  # Let the 2 jugs be called a,b
  a = state[0]
  b = state[1]
  r = randint(0, 5)

  if(a==8):
      ans.append(state)
      return True

  # if current state is already visited earlier
  if((a,b) in memory):
      return False
  
  memory[(a,b)] = 1
  while(1):
      if(r==0):   
          #fill jug a
          if(a==0):
              if(get_all_states((x,b))):
                  ans.append(state)
                  return True
          r = r + 1
          
      if(r==2):   
          #empty jug a into b
          if(a>0):
              if(get_all_states((max(0,a-(y-b)),min(y,a+b)))):
                  ans.append(state)
                  return True
          r = r + 1
          
      if(r==3): 
          #empty jug a into ground
          if(a>0):
              if(get_all_states((0,b))):
                  ans.append(state)
                  return True
          r = r + 1
          
      if(r==1): 
          #fill jug b
          if(b==0):
              if(get_all_states((a,y))):
                  ans.append(state)
                  return True
          r = r + 1
          
      if(r==4): 
          #empty jug b into a
          if(b>0):
              if(get_all_states((min(a+b,x), max(0,b-(x-a))))):
                  ans.append(state)
                  return True
          r = r + 1
          
      if(r==5):
          #empty jugb into ground
          if(b>0):
              if(get_all_states((a,0))):
                  ans.append(state)
                  return True
          r = 0
      
#initial_state = (0,0)    
          
a_init_value = int(input('Enter the initial value of a (the big jug) : ')) 
while( not(a_init_value in range(0,11))): 
    a_init_value = int(input('Enter the initial value of a (the big jug) : '))

b_init_value = int(input('Enter the initial value of b (the small jug) : '))  
while( not(b_init_value in range(0,7))): 
    b_init_value = int(input('Enter the initial value of a (the small jug) : '))                

#The while loops above are used to force the user to enter only the allowed size of the jugs      
   
initial_state = (a_init_value,b_init_value)
print("Starting the Non-deterministic search...")
get_all_states(initial_state)
ans.reverse()
a = a_init_value
b = b_init_value
print("start     : "+str(initial_state))
for i in ans:
  if(i[0] == a and i[1] == b):
      continue
  if(i[0] < a):
    if(a - i[0] == x and i[1] == b):
      print("Dump A    : "+str(i))
    else:
      print("Pour A->B : "+str(i))
  elif(i[0] - a == x):
    print("Fill A    : "+str(i))

  if(i[1] < b):
    if(b - i[1] == y and i[0] == a):
      print("Dump B    : "+str(i))
    else:
      print("Pour B->A : "+str(i))
  elif(i[1] - b == y):
    print("Fill B    : "+str(i))    
  a = i[0]
  b = i[1]