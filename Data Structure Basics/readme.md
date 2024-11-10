# Data Structures

## Queues
A **Queue** is a linear data structure that follows the **First In, First Out (FIFO)** principle. This means that elements are added to the rear (end) of the queue and removed from the front.

### Basic Operations
- **Enqueue**: Add an element to the end of the queue.
- **Dequeue**: Remove an element from the front of the queue.

### Queue Implementation
A queue can be implemented using either an **array** or a **linked list**.

### `enqueue()` Needs to:
- Accept a pointer to the queue.
- Accept the data type of the **VALUE** to be added to the queue.
- Add the data to the end of the queue.
- Update the size of the queue.

### `dequeue()` Needs to:
- Accept a pointer to the queue.
- Change the location of the front of the queue.
- Decrease the size of the queue.
- Return the value removed from the queue.

---

## Stacks
A **Stack** is a linear data structure that follows the **Last In, First Out (LIFO)** principle. This means that the most recently added element is the first one to be removed.

### Basic Operations
- **Push**: Add a new element to the top of the stack.
- **Pop**: Remove the most recently added element from the stack.

### Stack Implementation
A stack can be implemented using either an **array** or a **linked list**.

### Array-Based Stack

```c
typedef struct _stack {
    VALUE array[CAPACITY];
    int top;
} stack;
```

- **stack.s.top = 0**: The `top` variable indicates the position of the last inserted element.

### `push()` Needs to:
```c
void push(stack *s, VALUE val);
```
- Accept a pointer to the stack.
- Accept the data type of the **VALUE** to be added to the stack.
- Add the data to the stack at the top.
- Update the position of the `top` pointer.

### `pop()` Needs to:
```c
int x = pop(&s);
```
- Accept a pointer to the stack.
- Decrease the position of the `top` pointer.
- Return the value that was removed from the stack.

---

### Linked List-Based Stack

```c
typedef struct _stack {
    VALUE val;
    struct _stack *next;
} stack;
```

- A stack implemented with a linked list maintains a pointer to the head of the list.
  
### Operations:
- **Push**: Dynamically allocate a new node, set its pointer to point to the current head of the stack, then update the head pointer to the newly created node.
- **Pop**: Traverse to the second element, free the head node, and update the head pointer to point to the second element.

---

## Resizing Arrays
An **Array** is a contiguous block of memory. Resizing an array can be difficult due to the need to:
- Copy the array to a new location.
- Increase or decrease the array size.

### Downsides of Resizing:
- **Wasteful**: Frequent resizing can lead to wasted space.
- **Slow**: Copying large arrays is time-consuming.
- **Inefficient Iteration**: Resizing can lead to inefficiencies in array iteration (**O(n)** time complexity).

---

## Structures

**Structures (structs)** provide a way to group several variables of different types into a single variable. This allows you to create custom data types with meaningful names for better organization.

### Accessing Structure Members:
- You can access the members of a struct using the **dot (`.`) operator**.
- For a pointer to a struct, use the **arrow (`->`) operator** to access its members.

Example:

```c
struct person {
    char name[100];
    int age;
};

struct person p1;
p1.age = 30;
p1.name = "John";

struct person *p2 = &p1;
printf("%s is %d years old", p2->name, p2->age);
```

---

## Singly-Linked Lists

A **Singly-Linked List (SLL)** is a linear data structure where each element (node) contains two parts:
- **Data**: The value stored in the node.
- **Next Pointer**: A pointer to the next node in the list.

### Operations:
1. **Create Linked List**: Dynamically allocate nodes, initialize the `next` pointers.
2. **Search Linked List**: Traverse the list to find an element.
3. **Insert New Node**: Insert a node at the beginning of the list.
4. **Delete Node**: Remove a specific node from the list.
5. **Delete Entire Linked List**: Free all allocated memory.

### Create a Linked List:
```pseudocode
sllnode* create(VALUE val);
```
- Dynamically allocate space (using `malloc`).
- Initialize the `val` field with the given value.
- Set the `next` field to `NULL`.
- Return a pointer to the newly created node.

### Search for an Element:
```pseudocode
bool find(sllnode* head, VALUE val);
```
- Traverse the list starting from the head.
- If the current node's `val` matches the target value, return success.
- If you reach `NULL`, the value was not found.

### Insert a New Node:
```pseudocode
sllnode* insert(sllnode* head, VALUE val);
```
- Allocate space for the new node.
- Initialize the new node's fields.
- Insert the new node at the beginning of the list.
- Return a pointer to the new head of the list.

### Delete Entire Linked List:
```pseudocode
void destroy(sllnode* head);
```
- Recursively free each node in the list.
- Ensure memory is properly deallocated to avoid memory leaks.

---

## Doubly-Linked Lists

A **Doubly-Linked List (DLL)** allows traversal in both directions: forwards and backwards. This is possible because each node contains two pointers:
- **Next Pointer**: Points to the next node.
- **Previous Pointer**: Points to the previous node.

### Operations:
1. **Create Linked List**: Dynamically allocate nodes, initialize `next` and `prev` pointers.
2. **Search Linked List**: Traverse forwards or backwards to find an element.
3. **Insert New Node**: Insert a node at any position.
4. **Delete Node**: Remove a specific node from the list.
5. **Delete Entire Linked List**: Free all allocated memory.

### Insert a New Node:
```pseudocode
dllnode* insert(dllnode* head, VALUE val);
```
- Allocate space for the new node.
- Set the `next` pointer of the new node to point to the old head.
- Set the `prev` pointer of the old head to point to the new node.
- Update the head pointer to the new node.

### Delete a Node:
```pseudocode
void delete(dllnode* target);
```
- Update the `next` pointer of the previous node to skip the target node.
- Update the `prev` pointer of the next node to skip the target node.
- Free the memory of the target node.

---

## Hash Tables

A **Hash Table** combines the efficient random access of an array with the dynamic resizing ability of a linked list. Hash tables use a hash function to map keys to indices in an array.

### Basic Properties:
- **Insertion, Deletion, and Lookup**: All are typically **O(1)** operations.
- **Collisions**: Occur when two keys hash to the same index. Collision resolution can be done via:
  - **Linear Probing**: Place the data in the next available index.
  - **Chaining**: Use a linked list at each index to handle multiple values.

### Hash Function Requirements:
- Use the data being hashed.
- Be deterministic (same input always produces the same output).
- Distribute values uniformly across the table.

### Collision Handling:
- **Linear Probing**: Resolve collisions by checking subsequent positions until a free spot is found.
- **Chaining**: Resolve collisions by maintaining a linked list at each table index.

---

## Tries

A **Trie** is a tree-like data structure used for efficiently storing and searching a set of strings, such as a dictionary.

### Key Characteristics:
- Guaranteed to have a unique key for each element.
- Paths from the root node to a leaf node represent the stored data.
- **O(1)** time complexity for lookup, insertion, and deletion in an optimal implementation.

---
