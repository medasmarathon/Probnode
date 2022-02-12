from typing import List


def _get_alternatives_from_list_of_possible_items(possible_list: List[List[object]]):
  if len(possible_list) > 1:
    last_items = possible_list.pop()
    last_alternatives = _get_alternatives_from_list_of_possible_items(possible_list)
    if len(last_items) == 0:
      return last_alternatives
    if len(last_alternatives) == 0:
      return list(map(lambda x: [x], last_items))
    possible_chains = []
    for alternative in last_alternatives:
      for item in last_items:
        possible_chains.append(alternative + [item])
    return possible_chains
  elif len(possible_list) == 1:
    return list(map(lambda x: [x], possible_list[0]))