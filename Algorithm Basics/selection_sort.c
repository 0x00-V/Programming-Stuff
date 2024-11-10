#include <stdio.h>

void selection_sort(int arr[], int n);
void print_array(int arr[], int n);
int main()
{
    int arr[] = {40, 19, 69, 12, 2, 16, 9, 12, 12, 12, 8, 150, 256, 25, 256, 1};
    int n = sizeof(arr) / sizeof(arr[0]);

    printf("\nUnsorted Array: ");
    print_array(arr, n);

    // sort array
    selection_sort(arr, n);
    printf("Sorted array: ");
    print_array(arr, n);
    return 0;
}

void selection_sort(int arr[], int n)
{
    for(int i = 0; i < n - 1; i++)
    {
        // Lets first assume we hold current minimum value
        int min_index = i;

        // Iterate through unsorted parts to find minimum
        for(int j = i + 1; j < n; j++)
        {
            if(arr[j] < arr[min_index])
            {
                min_index = j; // update if smaller element found
            }
            
        }
        int temporary = arr[i];
        arr[i] = arr[min_index];
        arr[min_index] = temporary; 
    }   
}

void print_array(int arr[], int n)
{
    printf("{");
    for(int i = 0; i < n; i++)
    {
        printf("%d, ", arr[i]);
    }
    printf("}");
    printf("\n\n");
}