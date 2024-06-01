#!/usr/bin/env bash

set -e
echo "input flags ${1} ${2} ${3} ${4}"

# Usage create-vod-hls.sh SOURCE_FILE [OUTPUT_NAME]
[[ ! "${1}" ]] && echo "Usage: create-vod-hls.sh SOURCE_FILE [OUTPUT_NAME]" && exit 1

# comment/add lines here to control which renditions would be created
renditions=(
# resolution  bitrate  audio-rate
  "426x240    400k    64k"
  # "640x360    800k     96k"
  "842x480    1400k    128k"
  "1280x720   2800k    128k"
  # "1920x1080  5000k    192k"
)

segment_target_duration=10       # try to create a new segment every X seconds
max_bitrate_ratio=1.07          # maximum accepted bitrate fluctuations
rate_monitor_buffer_ratio=1.5   # maximum buffer size between bitrate conformance checks

#########################################################################

# first argument is the base path to the video file
# second argument is the path to the source video file
# third argument is the endpoint for the master playlist
# example: create-hls-vod.sh /path/to/video/dir path/to/video/file.mp4 endpoint
target="${1}" # absolute path to the target directory

source="${2}" # absolute path to the source video file

subtitle_path=${4}

mkdir -p ${target}

video_id=$(basename ${target})

key_frames_interval="$(echo `ffprobe ${source} 2>&1 | grep -oE '[[:digit:]]+(.[[:digit:]]+)? fps' | grep -oE '[[:digit:]]+(.[[:digit:]]+)?'`*2 | bc || echo '')"
key_frames_interval=${key_frames_interval:-50}
key_frames_interval=$(echo `printf "%.1f\n" $(bc -l <<<"$key_frames_interval/10")`*10 | bc) # round
key_frames_interval=${key_frames_interval%.*} # truncate to integer

# static parameters that are similar for all renditions
static_params="-c:a aac -ar 48000 -c:v h264 -profile:v main -crf 20 -sc_threshold 0"
static_params+=" -g ${key_frames_interval} -keyint_min ${key_frames_interval} -hls_time ${segment_target_duration}"
static_params+=" -hls_playlist_type vod"

# misc params
misc_params="-hide_banner -loglevel warning -y"

url=${3}

master_playlist="#EXTM3U\n#EXT-X-VERSION:3\n"

if [ -n "${subtitle_path}" ]; then
  master_playlist+="#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID=\"subs\",NAME=\"English Subtitles\",LANGUAGE=\"en\",AUTOSELECT=NO,DEFAULT=YES,FORCED=NO,URI=${url}/subs_playlist.m3u8\n"
fi


cmd=""
subtitle_cmd=""
renditionNo=0
for rendition in "${renditions[@]}"; do
  # if first rendition and subtitle path is provided
  if [ $renditionNo -eq 0 ] && [ -n "${subtitle_path}" ]; then
    subtitle_cmd="-i ${subtitle_path} -c:s webvtt"
  fi

  renditionNo=$((renditionNo+1))

  # drop extraneous spaces
  rendition="${rendition/[[:space:]]+/ }"

  # rendition fields
  resolution="$(echo ${rendition} | cut -d ' ' -f 1)"
  bitrate="$(echo ${rendition} | cut -d ' ' -f 2)"
  audiorate="$(echo ${rendition} | cut -d ' ' -f 3)"

  # calculated fields
  width="$(echo ${resolution} | grep -oE '^[[:digit:]]+')"
  height="$(echo ${resolution} | grep -oE '[[:digit:]]+$')"
  maxrate="$(echo "`echo ${bitrate} | grep -oE '[[:digit:]]+'`*${max_bitrate_ratio}" | bc)"
  bufsize="$(echo "`echo ${bitrate} | grep -oE '[[:digit:]]+'`*${rate_monitor_buffer_ratio}" | bc)"
  bandwidth="$(echo ${bitrate} | grep -oE '[[:digit:]]+')000"
  # name must be somehow prefixed with the s3 URL
  name="${height}p"
  endpoint="${3}/${name}.m3u8" # api endpoint for the master file
  
  # cmd+=" ${static_params} -vf scale=w=${width}:h=${height}:force_original_aspect_ratio=decrease"
  cmd+=" ${static_params} -vf scale=w=${width}:h=${height}"
  cmd+=" -b:v ${bitrate} -maxrate ${maxrate%.*}k -bufsize ${bufsize%.*}k -b:a ${audiorate}"
  cmd+=" -hls_segment_filename ${target}/${name}_%03d.ts ${target}/${name}.m3u8"
  
  # add rendition entry in the master playlist
  master_playlist+="#EXT-X-STREAM-INF:BANDWIDTH=${bandwidth},RESOLUTION=${resolution}"
  if [ -n "${subtitle_path}" ]; then
    master_playlist+=",SUBTITLE=\"subs\"" # add subtitle track
  fi
  master_playlist+="\n${endpoint}\n"

  # start conversion
  if [ -z "${subtitle_cmd}" ]; then
    echo -e "Executing command:\nffmpeg ${misc_params} -i ${source} ${cmd}\n"
    ffmpeg ${misc_params} -i ${source} ${cmd}
  else
    echo -e "Executing command:\nffmpeg ${misc_params} -i ${source} ${subtitle_cmd} ${cmd}\n"
    ffmpeg ${misc_params} -i ${source} ${subtitle_cmd} ${cmd}

    # rename the subtitle file from 240p_vtt.m3u8 to subs_playlist.m3u8
    mv ${target}/240p_vtt.m3u8 ${target}/subs_playlist.m3u8
  fi

  cmd=""
  subtitle_cmd=""
done

# create master playlist file
echo -e "${master_playlist}" > ${target}/playlist.m3u8

echo "Done - encoded HLS is at ${target}/"
