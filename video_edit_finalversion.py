from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings
import pygame
change_settings({"IMAGEMAGICK_BINARY": r"C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})

def add_info_box(video_path, output_path, font_name, duration, box_list, position):
    # Load the video
    video = VideoFileClip(video_path)
    width = video.w
    height = video.h
    print(width,height)
    #print(TextClip.list('color'))
    
    # Create the text clip
    subclip = video.subclip(0, 26)
    '''
    text_clip = (TextClip(box_text, fontsize=24, color='black', bg_color='white', font='Arial')
                 .set_position(position)
                 .set_duration(duration))
    '''
    # Create a box around the text
    '''
    box_clip = (TextClip(txt=" ", size=(text_clip.w + 50, text_clip.h + 50), color='white')
                .set_position((position[0] - 10, position[1] - 10))
                .set_duration(duration))
    '''
    #print ( TextClip.search('Arial-Bold', 'font') )
    txt_clip1 = TextClip(box_list[0],font=font_name, fontsize = 63, color = 'yellow')
    txt_clip1 = txt_clip1.set_start(6)
    txt_clip1 = txt_clip1.set_position((850,110)).set_duration(3)
    #txt_clip = txt_clip.set_pos(('right','center')).set_duration(5)  

    txt_clip2 = TextClip(box_list[1], font=font_name,fontsize = 80, color = 'yellow')
    txt_clip2 = txt_clip2.set_start(10)
    txt_clip2 = txt_clip2.set_position((100,110)).set_duration(3)

    txt_clip3 = TextClip(box_list[2],font=font_name, fontsize = 63, color = 'yellow')
    txt_clip3 = txt_clip3.set_start(14)
    txt_clip3 = txt_clip3.set_position((850,110)).set_duration(3)
    #txt_clip = txt_clip.set_pos(('right','center')).set_duration(5)

    txt_clip4 = TextClip(box_list[3],font=font_name, fontsize = 105, color = 'yellow')
    txt_clip4 = txt_clip4.set_start(23)
    txt_clip4 = txt_clip4.set_position((100,110)).set_duration(3)
    
    # Combine the box and text
    #info_box = CompositeVideoClip([video,txt_clip])
    info_box = CompositeVideoClip([subclip,txt_clip1,txt_clip2,txt_clip3,txt_clip4])
    
    # Add the info box to the video at the specified time
    #final_clip = CompositeVideoClip([video, info_box.set_start(start_time)])
    
    # Write the result to a file
    info_box.write_videofile(output_path, codec='libx264')
    
    # Close the clips
    video.close()
    #final_clip.close()

def on_mouse_move(x, y):
    print(f"Mouse position: ({x}, {y})")



# Usage example
video_path = "Renamed_files\\Final Boarding Call 720p.mp4"
output_path = "Renamed_files\\Final_Boarding_Call_720p_edited_check.mp4"
start_time = 5  # Start showing the box at 5 seconds
duration = 10  # Show the box for 10 seconds
box_text_airline = "AIR CANADA"
box_text_gate = "AC2490"
box_text_depcity = "VANCOUVER"
box_text_gatenum = "B16"
box_list = [box_text_airline,box_text_gate,box_text_depcity,box_text_gatenum]
position = (50,50)  # (x, y) coordinates for the top-left corner of the box
font_name= "Arial-Bold"
add_info_box(video_path, output_path, font_name, duration, box_list, position)

#video = VideoFileClip("All Groups Boarding.mp4")
#video.preview()
