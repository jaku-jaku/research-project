### Super Impose Video Frames:
# %% -------------------------------- Import Lib -------------------------------- %% #
import cv2
import numpy as np

from matplotlib import pyplot as plt
# ours:
from utils.uwarl_util import create_all_folders

def image_histogram_equalization(image, number_bins=256):
    # from http://www.janeriksolem.net/histogram-equalization-with-python-and.html

    # get image histogram
    image_histogram, bins = np.histogram(image.flatten(), number_bins, density=True)
    cdf = image_histogram.cumsum() # cumulative distribution function
    cdf = (number_bins-1) * cdf / cdf[-1] # normalize

    # use linear interpolation of cdf to find new pixel values
    image_equalized = np.interp(image.flatten(), bins[:-1], cdf)

    return image_equalized.reshape(image.shape), cdf
class VideoSuperMan:
    _video_dir  :str = ""
    _output_dir :str = ""
    _gap  = 120 # every X frames
    
    def __init__(self, video_dir, output_dir, gap):
        self._video_dir = video_dir
        self._output_dir = output_dir
        self._gap = gap
    
    def _create_subfolder(self, folder_name):
        path = f"{self._output_dir}/{folder_name}"
        create_all_folders(path)
        return path
        
    def super_impose(
        self, 
        filename:str, 
        if_skip_sampling:bool = False, 
        if_sampling_only:bool = False, 
        file_type:str=".mov", 
        step_size = 1,
    ):
        intermediate_output_path_ = self._create_subfolder(filename)
        file_path_ = f"{self._video_dir}/{filename}{file_type}"
        frame_count_  = self._sample_frames(file_path_, intermediate_output_path_, if_skip_sampling=if_skip_sampling)
        if if_sampling_only:
            return file_path_
        
        out_image_file_1 = self._impose_frames_from_directory(filename, frame_count_, intermediate_output_path_, self._output_dir, step_size=step_size, fg_alpha=[0.3,0.7], if_fwd=True, tag="_1")
        out_image_file_2 = self._impose_frames_from_directory(filename, frame_count_, intermediate_output_path_, self._output_dir, step_size=step_size, fg_alpha=[0.3,0.7], if_fwd=False, tag="_2")
        out_image_file_3 = self._impose_frames_from_directory(filename, frame_count_, intermediate_output_path_, self._output_dir, step_size=step_size, fg_alpha=[0.5,0.5], if_fwd=True, tag="_3")
        
        img1 = cv2.imread(out_image_file_1, cv2.IMREAD_UNCHANGED)
        img2 = cv2.imread(out_image_file_2, cv2.IMREAD_UNCHANGED)
        img3 = cv2.imread(out_image_file_3, cv2.IMREAD_UNCHANGED)
        new_img = cv2.addWeighted(img1, 0.5, img2, 0.5, 0)
        new_img = cv2.addWeighted(new_img, 0.5, img3, 0.5, 0)
        file_name = f"{self._output_dir}/super_{filename}.png"
        cv2.imwrite(file_name, new_img)
        return file_name
        
    def sample_video(
        self, 
        filename:str, 
        file_type:str=".mov", 
    ):
        intermediate_output_path_ = self._create_subfolder(filename)
        file_path_ = f"{self._video_dir}/{filename}{file_type}"
        self._sample_frames(file_path_, intermediate_output_path_, if_bkg_subtracation=False)
        
    #Extract frames from video into a folder
    def _sample_frames(self, file_path, intermediate_folder, 
        if_skip_sampling=False,
        t_offset = 0,
        image_crop_height_width = [[0,900],[500,1900]],
    ):
        vCap = cv2.VideoCapture(file_path)
        frame_count = 0
        tick = 0
        N_frames = vCap.get(cv2.CAP_PROP_FRAME_COUNT)
        indices_ = list(range(t_offset, int(N_frames), int(self._gap))) + [N_frames]
        N_samples = len(indices_)
        print("N_frames:",N_frames, " N_samples:", N_samples)
        
        if if_skip_sampling:
            return N_samples
        mask_ = None
        
        def _crop_image(frame):
            h0 = image_crop_height_width[0][0]
            h1 = image_crop_height_width[0][1]
            w0 = image_crop_height_width[1][0]
            w1 = image_crop_height_width[1][1]
            return frame[h0:h1, w0:w1]
        
        # fwd
        fgbg = cv2.createBackgroundSubtractorMOG2()
        for i in range(self._gap):
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                frame_ = _crop_image(frame)
                # - prep bkg subtraction:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
                fgmask = fgbg.apply(frame)
        
        positive_mask = {}
        frame_count = 0
        for i in indices_:
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                frame_ = _crop_image(frame)
                # apply mask:
                fgmask = fgbg.apply(frame_)
                fgmask0 = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
                frame_count += 1
                cv2.imwrite(f"{intermediate_folder}/frame_{frame_count}.png",frame_)
                # cv2.imwrite(f"{intermediate_folder}/pos_de_frame_{frame_count}.png",fgmask0)
                positive_mask[i] = fgmask0
                # create cumulated masks:
                if mask_ is not None:
                    mask_ = cv2.bitwise_or(mask_, fgmask0)
                else:
                    mask_ = fgmask0
        
        # rvr
        fgbg = cv2.createBackgroundSubtractorMOG2()
        for i in range(int(N_frames), int(N_frames - self._gap), -1):
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                # - prep bkg subtraction:
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
                frame = _crop_image(frame)
                fgmask = fgbg.apply(frame)
        
        frame_count = len(indices_) - 1
        indices_.reverse()
        for i in indices_:
            vCap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret,frame = vCap.read()
            if ret:
                frame_ = _crop_image(frame)
                # apply mask:
                fgmask = fgbg.apply(frame_)
                fgmask0 = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
                # cv2.imwrite(f"{intermediate_folder}/neg_de_frame_{frame_count}.png",fgmask0)
                avg_neg = np.average(fgmask0)
                avg_pos = np.average(positive_mask[i])
                if avg_pos < 1 or avg_neg < 1: # if one of the mask is empty, we or gate masks to retain features
                    mask_new = cv2.bitwise_or(positive_mask[i], fgmask0) # remove all noises
                    cv2.imwrite(f"{intermediate_folder}/de_frame_{frame_count}.png",mask_new)
                else:
                    mask_new = cv2.bitwise_and(positive_mask[i], fgmask0) # remove all noises
                    cv2.imwrite(f"{intermediate_folder}/de_frame_{frame_count}.png",mask_new)
                # (fix) decrement count after all:
                frame_count -= 1
                # create cumulated masks:
                if mask_ is not None:
                    mask_ = cv2.bitwise_or(mask_, fgmask0)
                else:
                    mask_ = fgmask0

        vCap.release()
        cv2.destroyAllWindows()
        
        # save cumulated masks:
        if mask_ is not None:
            path_frame = f"{intermediate_folder}/cumulated_de_frames.png"
            cv2.imwrite(path_frame, mask_)
        return len(indices_)

    def _impose_frames_from_directory(self, 
        filename, frame_count, 
        inter_folder, output_dir,
        t_start=1,
        if_fwd = True,
        if_cropping = True,
        fg_alpha=[0.3,0.7],
        step_size=1,
        tag="",
    ):
        output_file_name_ = f"{inter_folder}/super_{filename}{tag}.png"
        print(f"Super Imposing {frame_count} frames..")
        img_base_ = None
        mask_base_ = None
        if frame_count > 2:
            items = range(t_start, frame_count, step_size) if if_fwd else range(frame_count-step_size, t_start-step_size, -step_size)
            print(items)
            for i in items:
                print(">>> Overlapping frame:", i)
                img_new_ = cv2.imread(f"{inter_folder}/frame_{i}.png", cv2.IMREAD_UNCHANGED)
                mask_new_ = cv2.imread(f"{inter_folder}/de_frame_{i-1}.png", cv2.IMREAD_UNCHANGED)
                
                if img_new_ is None or mask_new_ is None:
                    print(f"X- Skipping {i} due to missing images!")
                    continue # skip

                _, mask_new_ = cv2.threshold(mask_new_, 5, 255, cv2.THRESH_BINARY)
                avg_ = np.average(mask_new_)

                print(img_new_.shape)
                print(mask_new_.shape)
                print(avg_)
                THRESHOLD_EMPTY_MASK = 1 # NOTE: need this to filter out static images with empty mask
                if avg_ < THRESHOLD_EMPTY_MASK:
                    print("X-  skipping due to invalid maskings (close to none)")
                    continue # skip
                if img_base_ is None:
                    img_base_ = img_new_
                    mask_base_ = mask_new_
                    continue # skip merging
                
                # merging process:
                pixel_changes_percent = np.count_nonzero(mask_new_ - mask_base_) / np.prod(np.shape(mask_new_))
                print(pixel_changes_percent)
                if pixel_changes_percent > 0.1: # only if the masks are drastically different >10%, otherwise it is a steady frame
                    jointed_mask = cv2.bitwise_or(mask_base_, mask_new_)
                    jointed_mask_inv_ = cv2.bitwise_not(jointed_mask)
                    mask_base_inv_ = cv2.bitwise_not(mask_base_)
                    mask_new_inv_ = cv2.bitwise_not(mask_new_)
                    # create staged foreground:
                    fg_new = cv2.bitwise_and(img_new_, img_new_, mask=mask_new_)
                    fg_base = cv2.bitwise_and(img_base_, img_base_, mask=mask_new_inv_)
                    fg = cv2.bitwise_or(fg_base, fg_new)
                    fg_new = cv2.bitwise_and(img_new_, img_new_, mask=mask_base_inv_)
                    fg_base = cv2.bitwise_and(img_base_, img_base_, mask=mask_base_)
                    fg2 = cv2.bitwise_or(fg_base, fg_new)
                    # blending forward and reversed images:
                    fg = cv2.addWeighted(fg2, fg_alpha[0], fg, fg_alpha[1], 0)
                    # combine foreground+background:
                    fg = cv2.bitwise_and(fg, fg, mask=jointed_mask)
                    bk = cv2.bitwise_and(img_base_, img_base_, mask=jointed_mask_inv_)
                    img_base_ = cv2.bitwise_or(fg, bk)
                    # visualization in notebook:
                    # plt.figure(); plt.imshow(fg);
                    # plt.figure(); plt.imshow(img_base_);

            # Next we stack our equalized channels back into a single image
            cv2.imwrite(output_file_name_, img_base_)
        
        return output_file_name_
        
        
#  ------------------------------- MAIN ----------------------------
def main_superImposed():
    king_ = VideoSuperMan(
        video_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1213",
        output_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1213/output",
        gap = 120
    )
    
    LIST_VIDEO_FILES = [
        # "Demo_1213_H_FWD",
        # "Demo_1213_H_RVR",
        # "Demo_1213_H_SPI",
        # "Demo_1213_H_CIR",
        # "Demo_1213_H_SQR",
        # "Demo_1213_H_TRI",
        # "Demo_1213_H_BEE",
        # #
        # "Demo_1213_E_FWD",
        # "Demo_1213_E_RVR",
        # "Demo_1213_E_SPI",
        # "Demo_1213_E_CIR",
        # "Demo_1213_E_SQR",
        # "Demo_1213_E_TRI",
        # "Demo_1213_E_BEE",
        # #
        # "Demo_1213_D_FWD",
        # "Demo_1213_D_RVR",
        # "Demo_1213_D_SPI",
        # "Demo_1213_D_CIR",
        # "Demo_1213_D_SQR",
        # "Demo_1213_D_TRI",
        # "Demo_1213_D_BEE",
        # #
        # "Demo_1213_U_FWD",
        # "Demo_1213_U_RVR",
        # "Demo_1213_U_SPI",
        # "Demo_1213_U_CIR",
        # "Demo_1213_U_SQR",
        # "Demo_1213_U_TRI",
        # "Demo_1213_U_BEE",
        # #
        "Demo_1213_LR_FWD",
        "Demo_1213_LR_RVR",
        "Demo_1213_LR_SPI",
        "Demo_1213_LR_CIR",
        "Demo_1213_LR_SQR",
        "Demo_1213_LR_TRI",
        "Demo_1213_LR_BEE",
        # #
        # "Demo_1213_UD_FWD",
        # "Demo_1213_UD_RVR",
        # "Demo_1213_UD_SPI",
        # "Demo_1213_UD_CIR",
        # "Demo_1213_UD_SQR",
        # "Demo_1213_UD_TRI",
        # "Demo_1213_UD_BEE",
    ]
    SAMPLING_ONLY = False #True #False
    SKIP_SAMPLING = not SAMPLING_ONLY
    
    # LIST_VIDEO_FILES = [
    #     # "Demo_1213_H_FWD",
    #     # "Demo_1213_E_RVR",
    #     "Demo_1213_U_BEE",
    #     # "Demo_1213_D_RVR",
    #     # "Demo_1213_LR_FWD",
    # ]
    # SAMPLING_ONLY = False
    # SKIP_SAMPLING = False
    # king_ = VideoSuperMan(
    #     video_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1127",
    #     output_dir="/Users/jaku/JX-Platform/Github_Research/dual-vins-data/demo_record/video_1127/output",
    #     gap = 10
    # )  
    
    # LIST_VIDEO_FILES = [
    #     "Demo_1127_Clips_UD_FWD",
    #     "Demo_1127_Clips_UD_RVR",
    #     "Demo_1127_Clips_UD_CIR",
    #     "Demo_1127_Clips_UD_CIR2",
    #     "Demo_1127_Clips_UD_BEE",
    #     "Demo_1127_Clips_UD_BEE2",
    #     "Demo_1127_Clips_UD_SQR",
    #     "Demo_1127_Clips_UD_TRI",
    # ]
    for file in LIST_VIDEO_FILES:
        print(" === Processing:", file, " === ")
        path = king_.super_impose(
            filename=file, file_type=".mp4", 
            if_skip_sampling=SKIP_SAMPLING, 
            if_sampling_only=SAMPLING_ONLY,
            step_size=1,
        )
        print(">>> Generated @", path)

def main_superSampling():
    king_ = VideoSuperMan(
        video_dir="/Users/jaku/JX-Learn/(Grad) UW/Advanced Robotis LAB/Demo-Videos/Demo-Multi-Floor/",
        output_dir="/Users/jaku/JX-Learn/(Grad) UW/Advanced Robotis LAB/Demo-Videos/Demo-Multi-Floor/output",
        gap = 600
    )  
    
    LIST_VIDEO_FILES = [
        "UWARL-Demo-Multi-Floor",
    ]
    for file in LIST_VIDEO_FILES:
        print(" === Processing:", file, " === ")
        path = king_.sample_video(filename=file, file_type=".mp4")
        print(">>> Generated @", path)


main_superImposed()
# main_superSampling()
