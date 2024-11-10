#include <stdlib.h>
#include <stdio.h>

typedef struct node
{
    int value;
    struct node* next;
} linkedlist_examp;

linkedlist_examp *createNewNode(int value);
void printlst(linkedlist_examp *head);
int main()
{
    linkedlist_examp *head = NULL;
    linkedlist_examp *tmp;

    for(int i = 21; i >= 0; i--)
    {
        tmp = createNewNode(i);
        tmp->next = head;
        head = tmp;
    }

    printlst(head);
}

linkedlist_examp *createNewNode(int value)
{
    linkedlist_examp *result = malloc(sizeof(linkedlist_examp));
    result->value = value;
    result->next = NULL;
    return result;
}


void printlst(linkedlist_examp *head)
{
    linkedlist_examp *tmp = head;

    while (tmp != NULL)
    {
        printf("%d - ", tmp->value);
        tmp=tmp->next;
    }
    printf("NULL\n");
    
}