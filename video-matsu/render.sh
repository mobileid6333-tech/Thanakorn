#!/bin/bash
# ตัดคลิป MATSU HAND ROLL TACO แนวตั้ง 9:16 ยาว 30 วินาที
set -e
SRC=/root/.claude/uploads/b982627e-a661-5c91-8e6b-77c2b9210699
OUT=$(cd "$(dirname "$0")" && pwd)
TMP=$OUT/parts; rm -rf $TMP; mkdir -p $TMP
FONT=$(fc-match -f '%{file}' 'Inter Display:style=ExtraBold')
FONT2=$(fc-match -f '%{file}' 'Inter:style=Medium')
LOOK="scale=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.12,fps=25"

# รายการช็อต: คลิป | เริ่ม | ยาว | เอฟเฟกต์ (none/zoom/end)
SHOTS="
08269 0.0 1.5 none
07755 4.0 1.0 none
07864 1.0 1.0 none
07756 0.0 1.5 none
07626 2.0 1.5 none
07629 2.5 1.0 none
07633 3.5 1.0 none
07648 0.0 1.0 none
07647 1.0 1.0 none
07753 1.5 2.0 none
07875 0.0 1.5 none
07755 2.0 1.0 none
07872 1.5 1.5 none
07841 3.0 1.5 none
07877 0.3 1.5 none
07878 3.0 1.5 none
07879 6.0 2.0 none
07756 2.0 2.5 zoom
08269 2.5 4.5 end
"
printf 'MATSU HAND ROLL TACO' > $TMP/t1.txt
printf 'WAMM MARKET FEST' > $TMP/t2.txt
printf '6–8 NOV  |  CENTRAL KHON KAEN' > $TMP/t3.txt

i=0; : > $TMP/list.txt
while read id ss dur fx; do
  [ -z "$id" ] && continue
  i=$((i+1)); f=$(ls $SRC/*$id*)
  VF="$LOOK"
  if [ "$fx" = zoom ]; then
    VF="$LOOK,scale=w='trunc(1080*(1+0.10*t/$dur)/2)*2':h=-2:eval=frame,crop=1080:1920"
  elif [ "$fx" = end ]; then
    A="alpha='min(1,max(0,(t-0.4)/0.5))'"
    VF="$LOOK,colorchannelmixer=rr=0.5:gg=0.5:bb=0.5,\
drawtext=fontfile=$FONT:textfile=$TMP/t1.txt:fontsize=76:fontcolor=white:x=(w-tw)/2:y=806:$A,\
drawbox=x=440:y=916:w=200:h=4:color=0xE8C27A@1:t=fill:enable='gte(t,0.6)',\
drawtext=fontfile=$FONT:textfile=$TMP/t2.txt:fontsize=58:fontcolor=0xFCD543:x=(w-tw)/2:y=946:alpha='min(1,max(0,(t-0.7)/0.5))',\
drawtext=fontfile=$FONT2:textfile=$TMP/t3.txt:fontsize=44:fontcolor=white:x=(w-tw)/2:y=1030:alpha='min(1,max(0,(t-1.0)/0.5))',\
fade=t=out:st=$(echo "$dur-0.4"|bc|sed "s/^\./0./"):d=0.4"
  fi
  ffmpeg -nostdin -v error -y -ss $ss -t $dur -i "$f" -vf "$VF" \
    -af "aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st=$(echo "$dur-0.05"|bc|sed "s/^\./0./"):d=0.05" \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -t $dur $TMP/p$i.mp4
  echo "file 'p$i.mp4'" >> $TMP/list.txt
done <<< "$SHOTS"

# จุดเปลี่ยนฉาก (วินาที) สำหรับให้กลองตีตรงจังหวะ
CUTS=$(echo "$SHOTS" | awk 'NF{printf "%s ", t+0; t+=$3}')
python3 $OUT/music.py $TMP/music.wav 29.96 $CUTS

# รวมภาพ + เพลง (ปิดเสียงจากกล้อง)
ffmpeg -nostdin -v error -y -f concat -safe 0 -i $TMP/list.txt -i $TMP/music.wav \
  -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]" \
  -map 0:v -map "[a]" \
  -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -r 25 -movflags +faststart \
  -c:a aac -b:a 192k -ar 48000 -t 29.96 \
  $OUT/MATSU_HandRollTaco_9x16.mp4
echo done
