#include <stdio.h>

int binary_search(int arr[], int low, int high, int x);
int main()
{
    int arr[] = {1,2,4,8,16,32,64,128,256,512,1024,2048};
    int n = sizeof(arr) / sizeof(arr[0]); // Dividing size of array by size of elements (usually 4). This will work out how many elements in the array.
    int x = 8;
    int result = binary_search(arr, 0, n-1, x);

    if(result == -1) printf("Value(%i) not found in array.\n", x);
    else printf("Value(%i) found: arr[%i].\n", x, result);
    return 0;
}
// this will be an iterative binary search 
int binary_search(int arr[], int low, int high, int x)
{
    while(low <= high)
    {
        int mid = low + (high - low) / 2;

        // This checks if value is at mid
        if(arr[mid] == x)
        {
            return mid;
        }

        // if left half is smaller than value, search right half
        if(arr[mid] < x)
        {
            low = mid+1;
        }else // value smaller, than right half, search left half
        {
            high = mid - 1;
        }
    }
    // If value not found in array, return -1.
    return -1;
}