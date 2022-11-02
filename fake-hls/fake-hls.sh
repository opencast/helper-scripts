#!/bin/bash

#Note: this temp dir grows without bounds.  Make sure it lives somewhere that can handle that...
temp=`mktemp -d`
#Create the docker container
nginx=`docker run --rm -d -v $temp:/tmp -v \`pwd\`/nginx.conf:/etc/nginx/nginx.conf:ro -p 8888:80 nginx:stable`
#Then start the stream, after making sure everyone can read and execute the temp directory
cd $temp
chmod -R a+rx $temp
ffmpeg -hide_banner \
  -re -f lavfi -i "
    testsrc2=size=1920x540:rate=25,
    drawbox=x=0:y=0:w=700:h=50:c=black@.6:t=fill,
    drawtext=x=  5:y=5:fontsize=54:fontcolor=white:text='%{pts\:gmtime\:$(date +%s)\:%Y-%m-%d}',
    drawtext=x=345:y=5:fontsize=54:fontcolor=white:timecode='$(date -u '+%H\:%M\:%S')\:00':rate=25:tc24hmax=1,
    setparams=field_mode=prog:range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709,
    format=yuv420p" \
  -re -f lavfi -i "
    sine=f=1000:r=48000:samples_per_frame='st(0,mod(n,5)); 1602-not(not(eq(ld(0),1)+eq(ld(0),3)))'" \
  -shortest \
  -fflags genpts \
  \
  -filter_complex "
    [0:v]drawtext=x=(w-text_w)-5:y=5:fontsize=54:fontcolor=white:text='1920x540':box=1:boxcolor=black@.6:boxborderw=5[v540p];
    [0:v]drawtext=x=(w-text_w)-5:y=5:fontsize=54:fontcolor=white:text='960x270':box=1:boxcolor=black@.6:boxborderw=5,scale=960x270[v270p]
  " \
  -map [v540p] \
  -map [v270p] \
  -map 1:a \
  \
  -c:v libx264 \
    -preset:v veryfast \
    -tune zerolatency \
    -profile:v main \
    -crf:v:0 23 -bufsize:v:0 2250k -maxrate:v:0 2500k \
    -crf:v:1 23 -bufsize:v:1  540k -maxrate:v:1  600k \
    -g:v 100000 -keyint_min:v 50000 -force_key_frames:v "expr:gte(t,n_forced*2)" \
    -x264opts no-open-gop=1 \
    -bf 2 -b_strategy 2 -refs 1 \
    -rc-lookahead 24 \
    -export_side_data prft \
    -field_order progressive -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
    -pix_fmt yuv420p \
  -c:a aac \
    -b:a 64k \
  \
  -f hls \
    -master_pl_name "master.m3u8" \
    -hls_list_size 5 \
    -hls_delete_threshold 1 \
    -hls_start_number_source epoch \
    -hls_fmp4_init_filename "init-%v.mp4" \
    -hls_segment_filename "chunk-stream-%v-%010d.mp4" \
    -hls_flags "+append_list+delete_segments+discont_start+program_date_time+independent_segments-temp_file" \
    -var_stream_map "a:0,name:audio-64k,agroup:audio,default:yes v:0,name:video-720p,agroup:audio v:1,name:video-360p,agroup:audio" \
    \
    -hls_time 6 \
    -hls_segment_type fmp4 \
    -hls_segment_options "movflags=+cmaf+dash+delay_moov+skip_sidx+skip_trailer" \
    "%v.m3u8"
#Stop the docker container
docker stop $nginx
#And remove the test files we've generated
rm -rf $temp /tmp/hls
