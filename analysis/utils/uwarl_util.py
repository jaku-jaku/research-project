import os
import rospy

def get_files(DIR:str, file_end:str=".bag"):
    return [ os.path.join(DIR, f) for f in os.listdir(DIR) if f.endswith(file_end) ]

def create_all_folders(DIR:str):
    if not (os.path.isdir(DIR)):
        rospy.logwarn("[uwarl_util] creating folder: " + DIR + "")
        os.makedirs(DIR)