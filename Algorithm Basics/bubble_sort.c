#include <stdio.h>


void swap(int* arr, int i, int j);
void bubble_sort(int arr[], int n);

int main()
{
    int arr[] = {9, 5, 1, 40, 10, 50, 666, 30, 36, 123, 60, 606, 404};
    int n = sizeof(arr) / sizeof(arr[0]);

    

    printf("\nUnsorted array: ");
    for(int i = 0; i < n; i++)
    {
        printf("%d, ", arr[i]); // print each element of array
    }
    printf("}\n");

    //Sort Array
    bubble_sort(arr, n);
    printf("\nSorted Array: {");
    for(int i = 0; i < n; i++)
    {
        printf("%d, ", arr[i]); // print each element of array
    }
    printf("}\n");
    return 0;
}


void swap(int* arr, int i, int j)
{
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}

void bubble_sort(int arr[], int n)
{
    // controls number of passes
    for(int i = 0; i < n - 1; i++)
    {
        // compares adjacent elements
        for(int j = 0; j < n - i - 1; j++)
        {
            // if current element > than next, swap them.
            if(arr[j] > arr[j+1])
            {
                swap(arr, j, j+1);
            }
        }
    }
}