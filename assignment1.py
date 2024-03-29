ALL_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)] # does not include diagonal movements

class Node:
  def __init__(self, position=None, parent=None, cost=1, g=0, f=0, h=0):
    self.position = position
    self.parent = parent
    self.cost = cost
    self.g = g # this is the true cost from start to current node
    self.f = f # this is the priority function that uses g and h
    self.h = h # this is the estimate from current node to goal (i'm gonna use manhattan)

  def __eq__(self, node):
    return self.position == node.position

  def print(self):
    print("Position: {} --- Parent: {} --- Cost: {} --- G: {} --- F: {} --- H: {}".format(self.position, self.parent, self.cost, self.g, self.f, self.h))

def pathfinding(input_filename, optimal_path_filename, explored_list_filename):
  # input_filename contains a CSV file with the input grid
  # optimal_path_filename is the name of the file the optimal path should be written to
  # explored_list_filename is the name of the file the list of explored nodes should be written to
  (grid, start, goals) = parseInputData(input_filename)
  
  start_node = Node(start, None, 0, 0, 0, 0)
  goal_list = []
  for goal in goals:
    goal_node = Node(goal, None, 0, 0, 0, 0)
    goal_list.append(goal_node)


  opened = []
  closed = []

  opened.append(start_node)

  while(opened):
    # pop current node off from the opened list
    cur_node = opened.pop(0)
    closed.append(cur_node)
    # check if we found our goal state
    for goal in goal_list:
      if cur_node == goal:
        optimal_path = []
        current = cur_node
        while current:
          optimal_path.append(current.position)
          current = current.parent
        optimal_path.reverse() # this is the optimal path to go from start to goal
        print("Visited:")
        for element in closed:
          print(element.position)

        # write to the 2 files and print the cost
        with open(optimal_path_filename, 'w') as file:
          for position in optimal_path:
            file.write(str(position))
            file.write('\n')
        with open(explored_list_filename, 'w') as file:
          for node in closed:
            file.write(str(node.position))
            file.write('\n')
        return cur_node.f # this returns the optimal path cost

    child_nodes = []
    for direction in ALL_DIRECTIONS:
      if not (((cur_node.position[0] + direction[0]) >= len(grid) or (cur_node.position[0] + direction[0]) < 0)
      or (cur_node.position[1] + direction[1] > (len(grid[len(grid)-1])-1) or cur_node.position[1] + direction[1] < 0)):
        if grid[cur_node.position[0] + direction[0]][cur_node.position[1] + direction[1]] != 'X':
          # we found a valid tile
          if (grid[cur_node.position[0] + direction[0]][cur_node.position[1] + direction[1]] == 'S') or \
            (grid[cur_node.position[0] + direction[0]][cur_node.position[1] + direction[1]] == 'G'):
            cost = 0
          else:
            cost = int(grid[cur_node.position[0] + direction[0]][cur_node.position[1] + direction[1]])

          new_node = Node(
            (cur_node.position[0] + direction[0], cur_node.position[1] + direction[1]),
            cur_node,
            cost
          )
          child_nodes.append(new_node)
    for child in child_nodes:
      closed_flag = False
      for closed_node in closed:
        if closed_node == child:
          closed_flag = True
      if not closed_flag:
        distance_list = []
        for goal in goal_list:
          distance = (abs(child.position[0] - goal.position[0]) + abs(child.position[1] - goal.position[1]))
          distance_list.append(distance)

        child.h = min(distance_list)
        child.g = cur_node.g + child.cost
        child.f = child.g + child.h
        opened_flag = False
        for opened_node in opened:
          if opened_node == child and opened_node.g < child.g:
            opened_flag = True
        if not opened_flag:
          for index in range(len(opened)):
            if child.f <= opened[index].f:
              opened.insert(index, child)
            if index == len(opened) - 1:
              opened.append(child)

          if len(opened) == 0:
            opened.append(child)
    print('\n\n')
  return -1
def parseInputData(input_filename):
  input_file = open(input_filename, 'r')
  lines = input_file.readlines()
 
  result = []
  for line in lines:
    row = []
    positions = line.split(',')
    for position in positions:
      row.append(position.strip())
    result.append(row)
  
  start = None
  goals = []
  for a in range(len(result)):
    for b in range(len(result[a])):
      if result[a][b] == 'S':
        start = (a,b)
      elif result[a][b] == 'G':
        goals.append((a,b))
  return (result, start, goals)


optimal_path_cost = pathfinding('./Example1/input.txt', './optimal_path.txt', './explored_list.txt')
print('The Optimal Path Cost is: {}'.format(optimal_path_cost))