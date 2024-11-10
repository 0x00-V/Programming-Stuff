#include <stdio.h>
#include <stdlib.h>

void merge(int arr[], int l, int m, int r);
void merge_sort(int arr[], int l, int r);
void print_array(int A[], int size);

int main()
{
    int arr[] = {25, 15, 59, 100, 110, 120, 69, 24, 1, 999, 150, 359};
    int arr_size = sizeof(arr) / sizeof(arr[0]);

    printf("\nUnsorted array: ");
    print_array(arr, arr_size);

    //sort array
    merge_sort(arr, 0, arr_size - 1);
    printf("\nSorted array: ");
    print_array(arr, arr_size);
}


// Merges two subarrays of arr[]
void merge(int arr[], int l, int m, int r)
{
    int i, j, k;
    int n1 = m - l + 1; // size of left subarray
    int n2 = r - m; // right subarray

    //temporary arrays
    int L[n1], R[n2];

    // Copy data to temp (Left and Right)
    for(i = 0; i < n1; i++)
    {
        L[i] = arr[l + i];
    }
    for(j = 0; j < n2; j++)
    {
        R[j] = arr[m + 1 + j];
    }


    // Merge temp arrays back into arr[l..r]
    i = 0;
    j = 0;
    k = l;
    

    // Merge elements from both subarrays
    while(i < n1 && j < n2) // continue until one subarray is done
    {
        if(L[i] <= R[j]) // comparison
        {
            arr[k] = L[i]; // copy smaller to arr
            i++; // move left
        } else
        {
            arr[k] = R[j]; // copy smaller to arr
            j++; // move right
        }
        k++; // next pos in merged arr
    }

    // Copy remaining elements of Left[]
    while(i < n1)
    {
        arr[k] = L[i]; 
        i++;
        k++;
    }

    // Copy remaining elements of Right[]
    while(j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }
}



// L = Left index and R = Right index if you couldn't tell already....

// These will be sorted here
void merge_sort(int arr[], int l, int r)
{
    if(l < r) // if more than one element
    {
        int m = l + (r - l) / 2; // middle point

        // Sort first and second halves
        merge_sort(arr, l, m); // sort left (recursion)
        merge_sort(arr, m+1, r); // sort right (recursion)

        merge(arr, l, m, r); // merge two sorted when done
    }
}


void print_array(int A[], int size)
{
    printf("{");
    for(int i = 0; i < size; i++)
    {
        printf("%d, ", A[i]);
    }
    printf("}\n");
}