
# Algorithms (Basics)

## Big O Notation
- **O(n²)** - Quadratic
- **O(n log n)** - n log n
- **O(n)** - Linear time
- **O(log n)** - Logarithmic
- **O(1)** - Constant time

### Complexity Classes
- **Big O (Upper bound - Worst case)**
- **Ω (Omega) (Lower bound - Best case)**
  - Ω(n²)
  - Ω(n log n)
  - Ω(n)
  - Ω(log n)
  - Ω(1)

- **θ (Theta) (Best and worst case - Same)**
  - θ(n²)
  - θ(n log n)
  - θ(n)
  - θ(log n)
  - θ(1)

***

## Linear Search
Search in a straight line with no skipping; iterate across the array from left to right.

```pseudocode
Repeat, starting at the first element:
    if first element == target, stop.
    Otherwise, move to the next element.
```

- **Worst case:** We have to look through the entire array: **O(n)**
- **Best case:** Might find the target instantly: **Ω(1)**

***

## Binary Search
A divide and conquer algorithm that reduces the search area by half each time. 

> **Note:** The array must be sorted first.

```pseudocode
Repeat until the array size is 0:
    Calculate the middle point of the current (sub)array.
    If the target is the middle element, stop.
    Otherwise, if the target is less than the middle, repeat with the left half.
    Otherwise, repeat with the right half.
```

- **Worst case:** The target element is found after repeatedly dividing the list of n elements: **O(log n)**
- **Best case:** The element is at the midpoint of the full array: **Ω(1)**

***

## Bubble Sort
Move higher-valued elements towards the right and lower ones towards the left.

```pseudocode
Set swap counter to a non-zero value.
Repeat until the swap counter is 0:
    Reset swap counter to 0.
    Look at each adjacent pair:
        If two adjacent elements are not in order, swap them and add one to the swap counter.
```

- **Worst case:** Array is in reverse order, requiring n passes to bubble each element: **O(n²)**
- **Best case:** Array is already sorted, resulting in no swaps: **Ω(n)**

***

## Selection Sort
Find the smallest unsorted element and add it to the end of the sorted list.

```pseudocode
Repeat until no unsorted elements remain:
    Search the unsorted part to find the smallest value.
    Swap the smallest found value with the first element of the unsorted part.
```

- **Worst case:** Iterate over each of the n elements n times: **O(n²)**
- **Best case:** Same as the worst case: **Ω(n²)**


## Merge Sort
Sort smaller arrays and merge them in sorted order. This algorithm leverages recursion.

```pseudocode
Sort the left half of the array.
Sort the right half of the array.
Merge the two halves.
```

- **Worst case:** Splitting and recombining n elements, resulting in a time complexity of: **O(n log n)**
- **Best case:** The array is already sorted, but a split and recombine still occurs: **Ω(n log n)**