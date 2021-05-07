from state import *

# Here you will implement evaluation functions. Recall that weighing components of your
# evaluation differently can have positive effects on performance. For example, you could
# have your evaluation prioritize running away from opposing agents instead of activiating
# switches. Also remember that for values such as minimum distance to have a positive effect
# you should inverse the value as _larger_ evaluation values are better than smaller ones.

# Helpful Functions:
# You may define any helper functions you want in this file.
# GameState.get_enemies() --> returns a list of opposing agent positions.
# GameState.get_boxes() --> returns a list of (row, col) positions representing where the boxes are on the map
# GameState.get_switches() --> returns a dictionary where the keys are the locations of the switches as (row, col) and the value
#                              being True if the switch is on and False if off.
# GameState.get_player_position() --> returns the current position of the player in the form (row, col)
# GameState.get_remaining_points() --> returns a list of the positions of the remaining armory points of the map in the form (row, col) 
  
class EvaluationFunctions:

  @staticmethod
  def euclidean_heuristic(p1, p2):
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5

  @staticmethod
  def score_evaluation(state):
    return state.get_score()
  
  @staticmethod
  def box_evaluation(state):
    # Question 4, your box evaluation solution goes here
    # Returns a numeric value evaluating the given state where the larger the better
    # raise NotImplementedError("Box Evaluation not implemented")
    boxes = state.get_boxes()
    player = state.get_player_position()
    enemies = state.get_enemies()
    point_distance = 0.000001 # to avoid 0 division error
    enemy_distance = 0
    switch_distance = 0.000001 # to avoid 0 division error
    switch = state.get_switches()
    for key in switch:
      switch_distance += EvaluationFunctions.euclidean_heuristic(player, key)
    for box in boxes:
      point_distance += EvaluationFunctions.euclidean_heuristic(player, box)
      for enemy in enemies:
        enemy_distance += EvaluationFunctions.euclidean_heuristic(player, enemy)
    if switch_distance == 0 and point_distance == 0:
      return enemy_distance
    elif switch_distance == 0:
      return 1 / point_distance + enemy_distance
    elif point_distance == 0:
      return 1 / switch_distance + enemy_distance
    else:
      return 1 / switch_distance + 1 / point_distance + enemy_distance

  @staticmethod
  def points_evaluation(state):
    # Question 5, your points evaluation solution goes here
    # eturns a numeric value evaluating the given state where the larger the better
    # raise NotImplementedError("Points Evaluation not implemented")
    player = state.get_player_position()
    points = state.get_remaining_points()
    enemies = state.get_enemies()
    point_distance = 0 # to avoid 0 division error
    enemy_distance = 0
    switch_distance = 0 # to avoid 0 division error
    switch = state.get_switches()
    for key in switch:
      switch_distance += EvaluationFunctions.euclidean_heuristic(player, key)
    for point in points:
      point_distance += EvaluationFunctions.euclidean_heuristic(player, point)
      for enemy in enemies:
        enemy_distance += EvaluationFunctions.euclidean_heuristic(player, enemy)
    if switch_distance == 0 and point_distance == 0:
      return enemy_distance + len(points)
    elif switch_distance == 0:
      return 1 / point_distance + enemy_distance + len(points)
    elif point_distance == 0:
      return 1 / switch_distance + enemy_distance + len(points)
    else:
      return 1 / switch_distance + 1 / point_distance + enemy_distance + len(points)