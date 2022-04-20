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

- Event does not have value. Only probability of event `P(Event("Raining")).value = 0.3` can be assigned value

- There are normal events, and `SureEvent`. Probability of`SureEvent` is always 1, and assigning value to probability of `SureEvent` will raise error

- Nodes, probabilities, events comparisons:

  - Events will be compared based on its name only

  - Probability compared based on its representation (type, value)

  - Nodes compared based on its underlying structure (its probability expressions, children nodes (respecting order))

  - `node.is_permutation_of(other)` will check if 2 nodes are permutations. For example: `N(P(event1)) + N(P(event2)) - N(P(event3))` is permutation of `N(P(event2)) - N(P(event3)) + N(P(event1))`

- Expansion returns a list of expanded nodes
- Contraction return a single contracted node
- Expansion and contraction will be done 1 time, not exhaustively until unexpandable / uncontractable

## Details

### Events

- Normal events

  `from probnode import Event`

- Sure events
  `from probnode import SureEvent`

### Probability

- Simple probability expression: Probability of a single event `P(Event("e1")`

- And probability expression, Or probability expression: Probability expression of 2 **probability expressions** (Thus, there is only a **And probability** of 2 probability of events, not **And probability** of 2 events.

  &#x274C; `P(Event("e1") & Event("e2"))`,

  &#x2705; use `P(P(Event("e1")) & P(Event("e2")))` instead )

- Conditional probability expression: Probability of X when Y `P(p1 // p2) ` (`p1` and `p2` are probability expressions)

      from probnode.probability import SimpleProbabilityExpression, AndProbabilityExpression, OrProbabilityExpression, ConditionalProbabilityExpression

### Node

- Normal node (Pure node): Node of a single probability expression

      from probnode.core import Node

- Chain node: a sum or product of nodes

  &#x2705; use `n1 + n2 - n3` to create `SumNode` instead of invoke directly `SumNode()` (`n1`, `n2`, `n3` can be either normal nodes or chain nodes)

  &#x2705; use `n1 * n2 / n3` to create `ProductNode` instead of invoke directly `ProductNode()` (`n1`, `n2`, `n3` can be either normal nodes or chain nodes)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/dangduc)
