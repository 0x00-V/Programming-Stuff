#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdbool.h>


#define MAX_NAME 256
#define TABLE_SIZE 10

typedef struct 
{
    char name[MAX_NAME];
    int age;
} person;

bool initHashTable();
unsigned int hash(char *name);
void print_table();
bool hash_table_insert(person *p);

int main(void)
{

    initHashTable();
    

    person dan = {.name="Dan", .age=14};
    person bob = {.name="Bob", .age=12};
    person jimmy = {.name="Jimmy", .age=6};

    hash_table_insert(&dan);
    hash_table_insert(&bob);
    hash_table_insert(&jimmy);
    print_table();
    return 0;
}

person *hash_table[TABLE_SIZE];

unsigned int hash(char *name)
{
    int len = strlen(name);
    unsigned int hash_val = 0;
    for(int i = 0; i < len; i++)
    {
        hash_val += name[i];
        hash_val = (hash_val*name[i]) % TABLE_SIZE;
    }
    return hash_val;
}


bool initHashTable()
{
    for(int i = 0; i < TABLE_SIZE; i++)
    {
        hash_table[i] = NULL;
        
    }
    return true;
}

void print_table()
{
    for(int i = 0; i < TABLE_SIZE; i++)
    {
        if(hash_table[i] == NULL)
        {
            printf("\t%i\t---\n",i);
        }
        else
        {
            printf("\t%i\t%s\n",i, hash_table[i]->name);
        }
    }
}

bool hash_table_insert(person *p)
{
    if(p == NULL) return false;
    int index = hash(p->name);
    if(hash_table[index] != NULL) return false;
    hash_table[index] = p;
    return true;
}