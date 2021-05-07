from state import *
from utils import *

class GameTreeSearching:
  # You will also find that the GameStateHandler class (already imported) will help perform needed operations on the
  # the game states. To declare a GameStateHandler simply wrap it around a GameState like such,
  # handler = GameStateHandler(GameState) where GameState will be an instance of GameState.
  
  # Below is a list of helpful functions:
  # GameStateHandler.get_successors() --> returns successors of the handled state
  # GameStateHandler.get_agents() --> returns a list of the positions of the agents on the map
  # GameStateHandler.get_agent_count() --> returns the number of agents on the map
  # GameStateHandler.get_agent_actions(agent_pos) --> returns a list of the possible actions the given agent can take
  # GameStateHandler.get_successor(agent_pos, action) --> returns the successor state if the given agent took the given action 
  # GameState.get_player_position() --> returns the players position in that game state as (row, col)
  # GameState.copy() --> returns a copy
  # GameState.is_win() --> returns True if the game state is a winning state
  # GameState.is_loss() --> returns True if the game state is a losing state

  # Hint:
  # To avoid unwanted issues with recursion and state manipulation you should work with a _copy_ of the state
  # instead of the original.

  @staticmethod
  def minimax_search(state, eval_fn, depth = 2):
    # Question 1, your minimax search solution goes here
    # Returns a SINGLE action based off the results of the search
    # raise NotImplementedError("Minimax search not implemented")
    def helper_minimax(state, eval_fn, index, depth):
      cur_state = state.copy()
      handler = GameStateHandler(cur_state)
      best_move = Direction.STOP
      if depth == 0 or cur_state.is_win() or cur_state.is_loss():
        return best_move, eval_fn(cur_state)
      if index == 0:
        value = -float("inf")
      else:
        value = float("inf")
      if index == 0:
        curr_agent = handler.get_agents()[index]
        for action in handler.get_agent_actions(curr_agent):
          state = handler.get_successor(curr_agent, action)
          nxt_move, nxt_val = helper_minimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth)
          if value < nxt_val:
            value, best_move = nxt_val, action   
      else:
        curr_agent = handler.get_agents()[index]
        for action in handler.get_agent_actions(curr_agent):
          state = handler.get_successor(curr_agent, action)
          if index == handler.get_agent_count() - 1:
            nxt_move, nxt_val = helper_minimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth - 1)
          else:
            nxt_move, nxt_val = helper_minimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth)
          if value > nxt_val:
            value, best_move = nxt_val, action
      return best_move, value
    
    move, value = helper_minimax(state, eval_fn, 0, depth)
    return move

  @staticmethod
  def alpha_beta_search(state, eval_fn, depth):
    # Question 2, your alpha beta pruning search solution goes here
    # Returns a SINGLE action based off the results of the search
    # raise NotImplementedError("Alpha Beta Pruning search not implemented")
    def helper_alpha_beta(state, eval_fn, index, depth, alpha, beta):
      cur_state = state.copy()
      handler = GameStateHandler(cur_state)
      best_move = Direction.STOP
      count = handler.get_agent_count()
      if depth == 0 or cur_state.is_win() or cur_state.is_loss():
        return best_move, eval_fn(cur_state)
      if index == 0:
        value = -float('inf')
      else:
        value = float('inf')

      position = handler.get_agents()[index]
      for action in handler.get_agent_actions(position):
        successor = handler.get_successor(position,action)
        if index == handler.get_agent_count() - 1:
          next_move, next_value = helper_alpha_beta(successor,eval_fn, 0, depth-1, alpha, beta)
        else:
          next_move, next_value=helper_alpha_beta(successor, eval_fn, index+1, depth, alpha, beta)
        if index == 0:
          if value < next_value:
            best_move, value = action, next_value
          if value >= beta:
            return best_move, value
          alpha = max(alpha,value)
        if index != 0:
          if value > next_value:
            best_move, value = action, next_value
          if value <= alpha:
            return best_move, value
          beta = min(beta,value)
        
      return best_move, value

    move, value = helper_alpha_beta(state, eval_fn, 0, depth, -float('inf'), float('inf'))
    return move 


  @staticmethod
  def expectimax_search(state, eval_fn, depth):
    # Question 3, your expectimax search solution goes here
    # Returns a SINGLE action based off the results of the search
    # raise NotImplementedError("Expectimax search not implemented")
    def helper_expectimax(state, eval_fn, index, depth):
      cur_state = state.copy()
      handler = GameStateHandler(cur_state)
      best_move = Direction.STOP
      if depth == 0 or cur_state.is_win() or cur_state.is_loss():
        return best_move, eval_fn(cur_state)
      if index == 0:
        value = -float("inf")
      else:
        value = float(0)
      if index == 0:
        curr_agent = handler.get_agents()[index]
        for action in handler.get_agent_actions(curr_agent):
          state = handler.get_successor(curr_agent, action)
          nxt_move, nxt_val = helper_expectimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth)
          if value < nxt_val:
            value, best_move = nxt_val, action   
      else:
        curr_agent = handler.get_agents()[index]
        possible_actions = len(handler.get_agent_actions(curr_agent))
        for action in handler.get_agent_actions(curr_agent):
          state = handler.get_successor(curr_agent, action)
          if index == handler.get_agent_count() - 1:
            nxt_move, nxt_val = helper_expectimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth - 1)
          else:
            nxt_move, nxt_val = helper_expectimax(state, eval_fn, (index + 1) % handler.get_agent_count(), depth)
          value += 1.0 / float(possible_actions) * nxt_val
      return best_move, value
    
    move, value = helper_expectimax(state, eval_fn, 0, depth)
    return move