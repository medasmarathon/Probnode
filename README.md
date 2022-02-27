# Probnode

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dangduc)


## Description
  Probability expression library

## Features
- Basic events and probability expressions modeling, similar to SymPy
- Calculation on a chain of probability expressions
- Contract and/or expand probability expressions chain, using probability mathematical characteristics

## Installation

    pip install probnode

## Quick Usage
- Events and probability modeling:
```    
  from probnode import Event, P

  e1 = Event("Sample event 1")
  p1 = P(e1)
  e2 = Event("Sample event 2")
  p2 = P(e2)
  
  p3 = P(p1 | p2) # Or Probability expression
  p4 = P(p1 & p2) # And Probability expression
  p5 = P(p1 // p2) # Conditional Probability expression

  # Display mathematical representation of the object(s)
  print(repr(p1))
```

- Mathematical treatment on probability expressions:
```
  # First convert probability expression to math node
  from probnode import N
  n1 = N(p1) # Each below is a (math) node
  n2 = N(p2)
  n3 = N(p3)
  n4 = N(p4)
  n5 = N(p5)

  # A sum of nodes
  snode = n1 + n2 - n4 
  # A product of nodes
  pnode = n5 * n2
```

- Contract/ expand mathematical chain of probability nodes

  - Contract
  ```
    from probnode.computation import contract

    c1 = contract(snode) # P(A) + P(B) - P(A and B) -> P(A or B)
    print(repr(c1))
    c2 = contract(pnode)
    print(repr(c2)) # P(A when B) * P(B) -> P(A and B)
  ```
  - Expand
  ```
    from probnode.computation import expand

    x = expand(n3)
    print(repr(x[0])) # P(A or B) -> P(A) + P(B) - P(A and B)
  ```

- Value calculations

    `node.value` will return the value of node
    
    If `node` is a chain node (comprising multiple nodes in sum / product mathematic operation), and either children `node.value` is not defined, the result parent `node.value` will be `None`

    `n1.value # None`

    Node value can be calculated from probability expression value
    ```
    p1.value = 0.7
    n1.value # equals 0.7
    ```
    Or by assigning value to itself
    ```
    n1.value = 0.6
    n1.value # equals 0.6
    ```
    The `value` assigned to itself takes precedence over the calculated `value` from its probability expression, or calculated from children nodes (if it is a chain node)

## Notes

- Nodes, probabilities, events comparisons:
  
  - Events will be compared based on its name only
  
  - Probability compared based on its representation (type, value)
  
  - Nodes compared based on its underlying structure (its probability expressions, children nodes (respecting order))

  - `node.is_permutation_of(other)` will check if 2 nodes are permutations

- Expansion returns a list of expanded nodes
- Contraction return a single contracted node
- Expansion and contraction will be done 1 time, not exhaustively until unexpandable / uncontractable


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dangduc)