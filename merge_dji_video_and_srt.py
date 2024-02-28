import os
import re
import subprocess

def merge_videos(video_files, output_file):
    # Build the ffmpeg command to concatenate the videos
    ffmpeg_command = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', 'temp.txt', '-c', 'copy', output_file]
    
    # Create a temporary file to list the sorted video files
    with open('temp.txt', 'w') as f:
        for file in video_files:
            f.write(f"file '{file}'\n")
    
    # Run ffmpeg command
    subprocess.run(ffmpeg_command)
    
    # Remove temporary file
    os.remove('temp.txt')

def merge_srt(subtitle_files, output_file):
    # Initialize merged subtitles
    merged_subtitles = []
    idx = 0
    time_shift = 0
    for file in subtitle_files:
        with open(file, 'r', encoding='ISO-8859-1') as f:  # Specify the correct encoding
            lines = f.readlines()
            # Extract the time shift from the first subtitle
            # Modify the subtitles' timing and append to merged_subtitles
            for line in lines:
                # print(line)
                try:
                    localIDX = int(line[:-1])
                    idx += 1
                    merged_subtitles.append(str(idx)+"\n")
                    continue
                except:
                    pass
                if re.match(r'\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+', line):
                    start, end = re.findall(r'\d+:\d+:\d+,\d+', line)
                    start_ms = timestamp_to_ms(start) + time_shift
                    end_ms = timestamp_to_ms(end) + time_shift
                    merged_subtitles.append(f"{ms_to_timestamp(start_ms)} --> {ms_to_timestamp(end_ms)}\n")
                    last_time_line = line.split("-->")[-1]
                else:
                    if "FrameCnt" in line:
                        # Regular expression pattern to match FrameCnt value
                        pattern = r'FrameCnt: (\d+)'
                        # Find FrameCnt value using regular expression
                        match = re.search(pattern, line)
                        if match:                          
                            # Replace the current FrameCnt value with the new value
                            replaced_line = re.sub(pattern, f'FrameCnt: {idx}', line)
                        merged_subtitles.append(replaced_line)
                    else:
                        merged_subtitles.append(line)
        time_shift += timestamp_to_ms(re.findall(r'\d+:\d+:\d+,\d+', last_time_line)[-1])
                
    # Write the merged subtitles to the output file
    with open(output_file, 'w') as f:
        f.writelines(merged_subtitles)


def timestamp_to_ms(timestamp):
    # Split timestamp by either ':' or ',' to handle different formats
    parts = re.split(r'[:,]', timestamp)
    h, m, s = map(int, parts[:3])
    ms = int(parts[3])
    return h * 3600000 + m * 60000 + s * 1000 + ms

def ms_to_timestamp(ms):
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

if __name__ == "__main__":
    # Define the path where video and subtitle files are located
    path = './'
    
    # Get all video files in the path and sort them by name
    video_files = sorted([os.path.join(path, file) for file in os.listdir(path) if file.endswith('.MP4')])
    
    # Ensure subtitle files are sorted in the same order
    subtitle_files = [file.replace('.MP4', '.SRT') for file in video_files]
    
    # Define the output files
    output_video_file = 'merged_videos.mp4'
    output_subtitle_file = 'merged_videos.srt'
    
    # Merge videos
    merge_videos(video_files, output_video_file)
    
    # Merge subtitles
    merge_srt(subtitle_files, output_subtitle_file)
