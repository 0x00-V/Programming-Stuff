#include <stdlib.h>
#include <stdio.h>

typedef struct node
{
    int data;
    struct node *prev;
    struct node *next;
} node;

node *createNode(int new_data);
void moveForward(node *head);
void moveBackwards(node *tail);
int main(void)
{
    node *head = createNode(1);
    node *second = createNode(2);
    node *third = createNode(3);
    node *fourth = createNode(4);

    head->next = second;
    second->prev = head;

    second->next = third;
    third->prev = second;

    third->next = fourth;
    fourth->prev = third;


    printf("Forward traversal in doubly-linked list:\n");
    moveForward(head);

    printf("Backwards traversal in doubly-linked list:\n");
    moveBackwards(fourth);

    free(head);
    free(second);
    free(third);
    free(fourth);
    return 0;
}


node *createNode(int new_data)
{
    node *new_node = (node *)
    malloc(sizeof(node));

    // Memory check
    if(new_node == NULL)
    {
        printf("Memory failed to allocate.\n");
        exit(1);
    }

    new_node->data=new_data;
    new_node->next=NULL;
    new_node->prev = NULL;
    return new_node;
}

void moveForward(node *head)
{
    node* current = head; // start
    
    // Continue until current node not null
    while(current != NULL)
    {
        printf("%d ", current->data);
        current = current->next;
    }
    printf("\n");
}

void moveBackwards(node *tail)
{
    node* current = tail;

    while(current != NULL)
    {
        printf("%d ", current->data);
        current = current->prev;
    }
    printf("\n");
}


