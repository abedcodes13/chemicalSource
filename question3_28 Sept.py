
# Group 51:





#========= 3.1 ========== 
#Question 1: Store the Data and Calculate Traveling Distance (Muhammed Abed)
import csv
import math


# Read the data from the CSV file and store it as a list of dictionaries
with open('water_data_q3.csv', 'r') as water_data:
    dict_reader = csv.DictReader(water_data)
    list_of_nodes = list(dict_reader)


#initiate flow rate and distance for each node
for node in list_of_nodes:
    node['flow rate'] = 0
    node['distance'] = 0





#create a dictionary with nodes and their linked nodes
riverSystem = {}
riverSystem[0]=[]
riverSystem[0].append(1)
for path in list_of_nodes:
    if path['water'] == 'Yes':
        for  i in list_of_nodes:
            if i['Node'] == path['linked'] and i['water'] == 'Yes':
                x = int(path["linked"])
                y = int(path["Node"])
                #checks if the start point of the current river segment is not already a key in the riverSystem dictionary. 
                # If it's not in the dictionary, it means that this is the first time this starting point is encountered.
                if  x not in riverSystem:
                    #If the start point is not in the dictionary,  initialize an empty list as the value for that key. 
                    # This list will be used to store the ending points of river segments that start at the same point.

                    riverSystem[x] = []
                #appends the end point of the current river segment to the list associated with the start point in the riverSystem dictionary. 
                # This creates a mapping between the starting point and all the ending points of river segments that originate from it.
                if y not in riverSystem[x]:
                    riverSystem[x].append(y)



#merge sort used to create a list in ascending order of node number
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    middle = len(arr) // 2
    left_half = arr[:middle]
    right_half = arr[middle:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    return merge(left_half, right_half)

def merge(left, right):
    result = []
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        left_node = int(left[left_index]['Node'])
        right_node = int(right[right_index]['Node'])

        if left_node < right_node:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result

# Sorting the list using merge sort
sorted_data = merge_sort(list_of_nodes)

#Create list containing only waterways.
river_nodes = []
for entry in sorted_data:
    if entry['water']=='Yes':
       river_nodes.append(entry)


#========= 3.3 ========== 
#Question 3

#Function to calculate distance between edge and a node
def distance_point_to_line(x, y, x1, y1, x2, y2):
    #calculate the differences between the coordinates of the point (x, y)
    #and the coordinates of one endpoint (x1, y1).

    A = x - x1
    B = y - y1
    #calculate the differences between the coordinates of the
    # two endpoints (x2 - x1 and y2 - y1).
    C = x2 - x1
    D = y2 - y1

    # calculate the dot product between vectors A and C and
    dot_product = A * C + B * D
    # find the squared length of vector CD
    length_squared = C * C + D * D
    # initialize a variable param to -1.
    param = -1

    #checks if the length_squared is not zero (to avoid division by zero)
    #and calculates the parameter param based on the dot product and the squared length.
    if length_squared != 0:
        param = dot_product / length_squared

    # calculate the coordinates (closest_x and closest_y) of the closest point on the 
    # line segment to the given point (x, y) based on the parameter param.
    if param < 0:
        closest_x, closest_y = x1, y1
    elif param > 1:
        closest_x, closest_y = x2, y2
    else:
        closest_x = x1 + param * C
        closest_y = y1 + param * D

    #calculate distance using Pythagoras' Theorem
    dx = x - closest_x
    dy = y - closest_y
    distance = math.sqrt(dx**2 + dy**2)
    return distance

#function to check if the junctions are connected directly to each other
def downstream_check(tuple_list, entries, start):
    child = tuple_list[start][0]
    if start == entries-1:
        return True
    #check if next junction in order is linked to current junction
    elif tuple_list[start+1][0] == int(river_nodes[child-1]['linked']):
            valid = downstream_check(tuple_list, entries, start+1) 
            if valid:
                return True
            else:
                return False	
    else:
        return False
    
#List all possible sources by seeing thhe headwaters connected to nodes. 
def possible_sources(tuple_list):
    sources=[]
    for i in tuple_list:
        for j in riverSystem[i[0]]:
            #since junctions cannot be a source, not added to list.
            if river_nodes[j-1]['type'] == 'headwater':
                sources.append([i[0],j])
    return sources


def chemical_source(tuple_list):
    entries = len(tuple_list)
    #returns True if junctions directly connected
    valid = downstream_check(tuple_list, entries, 0)
    max_conc = 0
    if valid:
        #If directly connected, junction with highest concentration is closest to source
        for i in tuple_list:
            if int(i[1])>max_conc:
                max_conc=int(i[1])
                closest_node=i[0]
        n1, n2 = riverSystem[closest_node][0], riverSystem[closest_node][1]
        if river_nodes[n1-1]['type'] == 'headwater' and river_nodes[n2-1]['type']=='headwater':
            return   n1, n2
        elif river_nodes[n1-1]['Type'] == 'headwater':
            return n1
        else:
            return n2
    
    #if not connected, checks distance between closest edge and junction
    #This is because chemical may have seeped
    else:
        #call function to list all possible sources and
        #the junctions they are connect to
        river_sources = possible_sources(tuple_list)

        min_dist = float('inf')
        closest_node = 0
        #Calculates distance between each node and possible edges
        for j in river_sources:
            
            dist=0 #reset distance
            hwater = j[1]
            junction = j[0]
            x1 = int(river_nodes[hwater-1]['x'])
            y1 = int(river_nodes[hwater-1]['y'])
            x2 = int(river_nodes[junction-1]['x'])
            y2 = int(river_nodes[junction-1]['y'])
            for i in tuple_list:
                node = int(i[0])
                x = int(river_nodes[node-1]['x'])
                y = int(river_nodes[node-1]['y'])
                dist += distance_point_to_line(x, y, x1, y1, x2, y2)
            if dist<min_dist:
                #update minimum distance and closest node
                min_dist = dist
                closest_node = int(j[1])
                
        return closest_node
            

chem_list = [(58,3),(55,10),(52,5)]
chem_list2 = [(57,10),(56,10),(55,2)]
print(chemical_source(chem_list))
print(chemical_source(chem_list2))
