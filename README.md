# Brachiograph - Raspberry Pi Gui and Identification

This project is archived as it has been finalized. Controls a brachiograph/plotter machine while giving a GUI and AI functioun for machine it runs off (Stable tested on Raspberry Pi). Disclaimer: The brachiograph.py file is an import from https://github.com/evildmp/BrachioGraph. The brachiographfinal.py is simply an extention I created for camera inputs, GUI, etc. If one wishes to see the function of this file, the instructions are listed on the base class's GitHub. From there, simply put this file in the same folder and execute. Some files such as yolo and other dependencies may be missing. 

#Instructions (Requried): https://www.brachiograph.art/
Class Imports and Details: 
```python
 
class BrachioGraph:

    def __init__(
        self,
        inner_arm=8,                # the lengths of the arms
        outer_arm=8,
        servo_1_centre=1600,        # shoulder motor centre pulse-width default is 1500
        servo_2_centre= 1480,        # elbow motor centre pulse-width default is 1500
        servo_1_angle_pws=[],       # pulse-widths for various angles
        servo_2_angle_pws=[],
        servo_1_degree_ms=-10,      # milliseconds pulse-width per degree
        servo_2_degree_ms=10,       # reversed for the mounting of the elbow servo
        arm_1_centre=-60,
        arm_2_centre=90,
        hysteresis_correction_1=13,  # hardware error compensation
        hysteresis_correction_2=5,
        bounds=[-8, 4, 6, 13],      # the maximum rectangular drawing area default [-8, 4, 6, 13]
        wait=None,
        virtual_mode = False,
        pw_up=1410,                 # pulse-widths for pen up/down
        pw_down=900,
    ):...
    #Line 19 brachiograph.py imported in brachiograph_final.py 
```

This project is simply for saving code as it was imported from a Raspberry Pi with uploading restrictions, thus the full project folder is nonexistent. Again, this project is depreciated and complete. 
