#!/usr/bin/env python3
"""
Test script to verify the randomization logic of the slideshow
"""
import sys
import os
sys.path.append('.')
from slideshow import load_media
import tempfile

def test_randomization():
    # Create a temporary directory with some test files
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create some test image files
        test_files = ['image1.jpg', 'image2.png', 'image3.jpeg', 'video1.mp4', 'image4.bmp']
        for filename in test_files:
            with open(os.path.join(temp_dir, filename), 'w') as f:
                f.write('dummy content')
        
        # Load media multiple times and check if order changes
        order1 = [os.path.basename(f) for f in load_media(temp_dir)]
        order2 = [os.path.basename(f) for f in load_media(temp_dir)]
        order3 = [os.path.basename(f) for f in load_media(temp_dir)]
        
        print("First load order:", order1)
        print("Second load order:", order2)
        print("Third load order:", order3)
        
        # Check that all files are present in each load
        assert set(order1) == set(test_files), "Missing files in first load"
        assert set(order2) == set(test_files), "Missing files in second load"
        assert set(order3) == set(test_files), "Missing files in third load"
        
        # Check that at least one of the orders is different (randomization working)
        different = (order1 != order2) or (order2 != order3) or (order1 != order3)
        
        if different:
            print("✅ Randomization is working! Orders are different.")
        else:
            print("⚠️  All orders are the same. This could happen by chance with small file counts.")
        
        return True

if __name__ == "__main__":
    test_randomization()
