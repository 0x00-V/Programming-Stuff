#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
 
#define BLK_SIZE 512

int main(int argc, char *argv[])
{
    // Accept single cli args
     if(argc != 2) 
     {
        printf("Usage: ./recover FILE\n");
        return 1;
     }
     // Open memory card, and check if found.
     FILE *card = fopen(argv[1], "r");
     if(!card)
     {
        printf("Couldn't locate file\n");
        return 1;        
     }

     // Buffer for block of data
     uint8_t buffer[BLK_SIZE];
     int jpegFileCount = 0; // Keep track of how many jpegs that have been discovered
     FILE *jpeg = NULL;
    
     //While there's still data left to read from the memory card
     while(fread(buffer, 1, BLK_SIZE, card) == BLK_SIZE)
     {
        // Check JPEG header
        if(buffer[0] == 0xFF && buffer[1] == 0xD8 && buffer[2] == 0xFF && (buffer[3] & 0xF0) == 0xE0) /* (16 diff vals. Unecessary code) Using 
        bitwise arithmetic. | look at first 4 bits of 8 bit byte, set remaining 4 bits to 0. All will  become 0xe0*/
        {
        // Ensure no JPEG file is currently open
        if(jpeg != NULL) fclose(jpeg);
        // Create JPEGs from the data
        char filename[8];
        sprintf(filename, "%03d.jpg", jpegFileCount);
        jpeg = fopen(filename, "w");
        if(jpeg == NULL)
        {
            printf("Couldn't create file %s\n", filename);
            fclose(card);
            return 1;
        }
        jpegFileCount++;
        // Check if we have file open, if so. Write.
        }
        if(jpeg != NULL) fwrite(buffer, 1, BLK_SIZE, jpeg);
     }
     // When eof close all files
     if(jpeg != NULL) fclose(jpeg);
     fclose(card);
     return 0;
        
}


