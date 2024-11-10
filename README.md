# Water Network Analysis - Question 3 Solution

This repository contains the solution to **Question 3** of the Water Network Assignment, focusing on identifying the likely source of chemical compounds in a river network. The project leverages Python to analyze chemical concentrations across different junctions in the river and estimate the origin based on connectivity and proximity of headwater sources.

## Project Overview

In this assignment, water flows through a network of nodes representing headwaters, junctions, and gauging stations. The primary objective of Question 3 is to identify the most likely headwater source of a given chemical mix, even accounting for possible seepage from other headwaters.

### Key Functionalities

1. **Data Storage & Distance Calculation**:
   - Reads data from a CSV file (`water_data_q3.csv`) to map nodes and their connections.
   - Initializes flow rates and distances between nodes.
  
2. **River System Mapping**:
   - Creates a dictionary (`riverSystem`) to store river segments and connected nodes for efficient traversal.
   - Utilizes a **merge sort algorithm** to sort nodes in ascending order based on node IDs.

3. **Distance Calculation**:
   - Includes `distance_point_to_line`, a function to calculate the distance from a node to an edge, aiding in determining seepage proximity.

4. **Source Identification**:
   - `chemical_source`: Analyzes junctions to determine the likely headwater source of a given chemical sequence, considering:
     - Directly connected nodes
     - Proximity to headwater nodes if direct connections are not established

### Functions

- **`distance_point_to_line(x, y, x1, y1, x2, y2)`**: Calculates the distance from a node to a line segment between two nodes.
- **`downstream_check(tuple_list, entries, start)`**: Verifies if nodes are directly connected downstream.
- **`possible_sources(tuple_list)`**: Lists possible headwater sources for given river segments.
- **`chemical_source(tuple_list)`**: Determines the most likely source of a chemical composition given its concentration at various nodes.

### Example Usage

```python
chem_list = [(58, 3), (55, 10), (52, 5)]
chem_list2 = [(57, 10), (56, 10), (55, 2)]

print(chemical_source(chem_list))  # Output: Headwater node number(s)
print(chemical_source(chem_list2)) # Output: Headwater node number(s)
```

## Assumptions

The approach assumes:
- River flow is unidirectional, from headwaters to downstream.
- Data from CSV (`water_data_q3.csv`) is structured with necessary node connectivity and type details.
- Seepage may influence chemical concentrations if nodes are not directly connected.

## Setup

1. **Requirements**: Python 3.x
2. **File Structure**:
   - `water_data_q3.csv`: CSV file containing data on nodes, connectivity, and type.

3. **Running the Solution**:
   - Run the Python script to execute `chemical_source` and obtain the likely headwater source of a given chemical composition.

## Future Improvements

- Extending the script to handle multiple sources and analyze chemical mixing at junctions.
- Implementing visualization tools for mapping river paths and concentration levels.
