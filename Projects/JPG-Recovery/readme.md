# JPEG File Recovery Program

This program is designed to recover JPEG files from a raw memory card or disk image, typically in cases where the storage medium is corrupted, or you want to extract individual files from a raw image of the storage device.

It works by scanning through the raw data for JPEG headers (`0xFF 0xD8 0xFF`), and when it finds one, it assumes the following data belongs to the same JPEG file. It will then write the recovered JPEG data to a new file.

## Features
- Recovers JPEG files from a raw image or memory card dump.
- Automatically detects JPEG file headers and reconstructs files.
- Creates a separate JPEG file for each detected image.
- Uses a 512-byte block size for reading the memory card.

## Requirements
- C compiler (e.g., GCC)
- A raw image of the memory card (e.g., `image.raw`) or any other binary data file that contains JPEG fragments.

## How It Works
The program works by:
1. Opening the raw image file provided as a command line argument.
2. Reading the file in 512-byte blocks.
3. Searching each block for the JPEG header (`0xFF 0xD8 0xFF`).
4. Once a JPEG header is found, it creates a new JPEG file and writes the data to it.
5. It continues writing data to the JPEG file until another JPEG header is found or the end of the file is reached.
6. Each detected JPEG file is saved as `XXX.jpg` (where `XXX` is a 3-digit number, starting from `000`).

