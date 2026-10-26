import os
import sys
import subprocess

SAMPLES = {
    "1": ("Current Voice (Deep Indian Male)", r"C:\Users\USER\Desktop\Voice_Sample_1_Prabhat_Indian_Male_Deep.mp3"),
    "2": ("Smooth Indian Female", r"C:\Users\USER\Desktop\Voice_Sample_2_Neerja_Indian_Female_Smooth.mp3"),
    "3": ("Expressive Indian Storyteller Female", r"C:\Users\USER\Desktop\Voice_Sample_3_Neerja_Expressive_Storyteller.mp3"),
    "4": ("Deep US Documentary Male (NatGeo / Vox)", r"C:\Users\USER\Desktop\Voice_Sample_4_Christopher_US_Documentary_Male.mp3"),
    "5": ("Warm Conversational US Male", r"C:\Users\USER\Desktop\Voice_Sample_5_Guy_US_Conversational_Male.mp3"),
    "6": ("Expressive US Female", r"C:\Users\USER\Desktop\Voice_Sample_6_Aria_US_Expressive_Female.mp3"),
    "7": ("BBC Documentary British Male", r"C:\Users\USER\Desktop\Voice_Sample_7_Ryan_British_BBC_Documentary_Male.mp3"),
}

def play_sample(num="4"):
    if num in SAMPLES:
        desc, path = SAMPLES[num]
        print(f"🔊 Playing [{num}]: {desc}")
        os.startfile(path)
    else:
        print("Invalid sample number! Choose 1 through 7.")

if __name__ == "__main__":
    choice = sys.argv[1] if len(sys.argv) > 1 else "4"
    play_sample(choice)
