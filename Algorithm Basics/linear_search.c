#include <stdio.h>

int linear_search(int arr[], int size, int valWeWant);
int main()
{
    int arr[] = {25, 40, 10, 79, 194, 43, 69, 28, 21, 39, 20};
    int valueWeWantToFind = 43;
    printf("We are looking for %i in arr\n", valueWeWantToFind);
    
    // Pass in array, size of array (how many elements), and the value we want to find.
    int answer = linear_search(arr, 11, valueWeWantToFind);
    if(answer >= 0)
    {
        printf("Found %i at arr[%i].\n", valueWeWantToFind, answer);
    }
    else
    {
        printf("Couldn't find %i in arr.\n", valueWeWantToFind);
    }
    return 0;
}


int linear_search(int arr[], int size, int valWeWant)
{
    // for each element in array
    for(int i = 0; i < size; i++)
    {
        // if we find the value we want in current index. Return the index number.
        if(valWeWant == arr[i])
        {
            // exitits early
            return i;
        }
    }
    // if we don't find value. Return -1 to indicate we couldn't locate it.
    return -1;
}