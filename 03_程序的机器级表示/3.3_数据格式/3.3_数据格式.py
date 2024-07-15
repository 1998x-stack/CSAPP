# 3.3_数据格式

"""
Lecture: 03_程序的机器级表示/3.3_数据格式
Content: 3.3_数据格式
"""

import numpy as np
import sys
from typing import Tuple

class DataFormats:
    """
    Class to demonstrate data formats using NumPy.
    
    Attributes:
        int_array (np.ndarray): NumPy array of integers for demonstration.
        float_array (np.ndarray): NumPy array of floats for demonstration.
    """
    
    def __init__(self, int_values: Tuple[int, int, int], float_values: Tuple[float, float, float]):
        """
        Initialize the DataFormats class with integer and float values.
        
        Args:
            int_values (Tuple[int, int, int]): Tuple of three integers.
            float_values (Tuple[float, float, float]): Tuple of three floats.
        """
        self.int_array = np.array(int_values, dtype=np.int32)
        self.float_array = np.array(float_values, dtype=np.float64)
    
    def display_sizes(self):
        """
        Display sizes of integer and float arrays.
        """
        print("Sizes of Arrays:")
        print("================")
        print(f"Int Array: {self.int_array.size} elements of {self.int_array.dtype} each")
        print(f"Float Array: {self.float_array.size} elements of {self.float_array.dtype} each")
    
    def display_memory_layout(self):
        """
        Display memory layout and alignment of arrays.
        """
        print("\nMemory Layout and Alignment:")
        print("============================")
        print(f"Int Array Memory Layout:\n{self.int_array}")
        print(f"Float Array Memory Layout:\n{self.float_array}")
    
    def check_endianness(self):
        """
        Check the endianness of the system using NumPy.
        """
        if sys.byteorder == 'little':
            print("\nSystem Endianness: Little Endian")
        else:
            print("\nSystem Endianness: Big Endian")
        
        # NumPy's byte order for the integer array
        int_byte_order = self.int_array.dtype.byteorder
        print(f"Int Array Byte Order (NumPy): {int_byte_order}")
        
        # NumPy's byte order for the float array
        float_byte_order = self.float_array.dtype.byteorder
        print(f"Float Array Byte Order (NumPy): {float_byte_order}")

# Example usage
if __name__ == "__main__":
    # Initialize DataFormats object with example values
    data_formats = DataFormats((10, 20, 30), (1.5, 2.5, 3.5))
    
    # Display sizes of arrays
    data_formats.display_sizes()
    
    # Display memory layout and alignment
    data_formats.display_memory_layout()
    
    # Check endianness
    data_formats.check_endianness()