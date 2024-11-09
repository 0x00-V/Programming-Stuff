#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <stdbool.h>
#include <ctype.h>
#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next; 
} node;

const unsigned int N = 27;
node *table[N]; 
int wrd_cnt = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    int hash_val = hash(word);
    node *cursor = table[hash_val];
    
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0){ return true; }
        cursor = cursor->next;
    }
    
    return false;
}

// Hashes word to a number (returns an index from 0 to N-1)
unsigned int hash(const char *word)
{
    if (isalpha(word[0])) {
        return toupper(word[0]) - 'A';
    } else {
        return N - 1;
    }
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    for (int i = 0; i < N; i++) {
        table[i] = NULL; 
    }

    FILE *file = fopen(dictionary, "r");
    if (file == NULL) {
        return false;
    }

    char wrd_buffer[LENGTH + 1];
    while (fscanf(file, "%s", wrd_buffer) != EOF)
    {
        node *n_word = malloc(sizeof(node));
        if (n_word == NULL) {
            fclose(file);
            return false;
        }

        int hash_val = hash(wrd_buffer);
        strcpy(n_word->word, wrd_buffer);
        n_word->next = table[hash_val];
        table[hash_val] = n_word;  

        wrd_cnt++;
    }

    fclose(file);
    return true; 
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void){ return wrd_cnt; }

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next; 
            free(temp); 
        }
    }
    return true;
}
