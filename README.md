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
  pnode = n3 * n2
```

- Contract/ expand mathematical chain of probability nodes

  - Contract
  ```
    from probnode.computation.contract import contract

    c = contract(snode)
    print(repr(c))
  ```
  - Expand
  ```
    from probnode.computation.expand import expand

    x = expand(n3)
    print(repr(x[0]))
  ```

## More In-depth Detail


[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dangduc)