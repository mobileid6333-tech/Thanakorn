#!/bin/bash
# คลิปที่ 2: MATSU HAND ROLL TACO แนว FOMO "เหลืออีก 2 วันสุดท้าย!" ยาว 24.5 วินาที
set -e
SRC=/root/.claude/uploads/b982627e-a661-5c91-8e6b-77c2b9210699
OUT=$(cd "$(dirname "$0")" && pwd)
TMP=$OUT/parts2; rm -rf $TMP; mkdir -p $TMP
TH=$OUT/fonts/Kanit-ExtraBold.ttf
EN=$(fc-match -f '%{file}' 'Inter Display:style=ExtraBold')
EN2=$(fc-match -f '%{file}' 'Inter:style=Medium')
YEL=0xFCD543
LOOK="scale=1080:1920,setsar=1,eq=contrast=1.06:saturation=1.12,fps=25"
TOTAL=24.46

# ช่วงเวลาแต่ละส่วน (ให้เพลงเปลี่ยนตาม): FOOD HERO เริ่ม 3 วิ, EVENT VIBE เริ่ม 10 วิ
SECTIONS=3,10

# คลิป | เริ่ม | ยาว | ชนิด (none / hook = มีข้อความต้นคลิป / zoom = ภาพเด่น+ข้อความ / end = ปิดท้าย)
SHOTS="
07756 0.0 1.0 hook
07755 4.0 1.0 hook
07875 0.0 1.0 hook
07626 2.0 1.0 none
07633 3.5 0.5 none
07629 3.5 1.0 none
07648 0.0 1.0 none
07753 1.5 1.5 none
07755 2.0 1.0 none
07756 1.0 1.0 none
08269 0.0 1.5 none
07872 1.5 1.0 none
07864 1.0 1.0 none
07841 3.0 1.5 none
07877 0.3 1.0 none
07878 3.0 1.0 none
07879 6.0 1.0 none
07841 0.0 1.5 none
07756 2.5 2.0 zoom
07879 2.5 3.0 end
"
printf 'เหลืออีก 2 วันสุดท้าย!' > $TMP/hook.txt
printf 'ยังไม่ได้ลอง ต้องมาแล้ว!' > $TMP/cta.txt
printf 'MATSU HAND ROLL TACO' > $TMP/t1.txt
printf '7–8 NOV  |  CENTRAL KHON KAEN' > $TMP/t3.txt

BOX="box=1:boxcolor=black@0.55:boxborderw=28"
i=0; first=1; : > $TMP/list.txt
while read id ss dur fx; do
  [ -z "$id" ] && continue
  i=$((i+1)); f=$(ls $SRC/*$id*)
  VF="$LOOK"
  if [ "$fx" = hook ]; then
    A=1; [ $first = 1 ] && A="'min(1,t/0.15)'"; first=0
    VF="$LOOK,drawtext=fontfile=$TH:textfile=$TMP/hook.txt:fontsize=88:fontcolor=$YEL:$BOX:x=(w-tw)/2:y=h*0.20:alpha=$A"
  elif [ "$fx" = zoom ]; then
    VF="$LOOK,scale=w='trunc(1080*(1+0.10*t/$dur)/2)*2':h=-2:eval=frame,crop=1080:1920,\
drawtext=fontfile=$TH:textfile=$TMP/cta.txt:fontsize=84:fontcolor=$YEL:$BOX:x=(w-tw)/2:y=h*0.20:alpha='min(1,t/0.15)'"
  elif [ "$fx" = end ]; then
    VF="$LOOK,colorchannelmixer=rr=0.85:gg=0.85:bb=0.85,drawbox=x=0:y=1150:w=1080:h=390:color=black@0.62:t=fill,\
drawtext=fontfile=$TH:textfile=$TMP/cta.txt:fontsize=72:fontcolor=$YEL:x=(w-tw)/2:y=1190,\
drawbox=x=440:y=1310:w=200:h=4:color=$YEL@1:t=fill:enable='gte(t,0.3)',\
drawtext=fontfile=$EN:textfile=$TMP/t1.txt:fontsize=76:fontcolor=white:x=(w-tw)/2:y=1345:alpha='min(1,max(0,(t-0.3)/0.4))',\
drawtext=fontfile=$EN2:textfile=$TMP/t3.txt:fontsize=44:fontcolor=white:x=(w-tw)/2:y=1450:alpha='min(1,max(0,(t-0.6)/0.4))',\
fade=t=out:st=$(echo "$dur-0.4"|bc|sed "s/^\./0./"):d=0.4"
  fi
  ffmpeg -nostdin -v error -y -ss $ss -t $dur -i "$f" -vf "$VF" -an \
    -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -t $dur $TMP/p$i.mp4
  echo "file 'p$i.mp4'" >> $TMP/list.txt
done <<< "$SHOTS"

CUTS=$(echo "$SHOTS" | awk 'NF{printf "%s ", t+0; t+=$3}')
SECTIONS=$SECTIONS python3 $OUT/music.py $TMP/music.wav $TOTAL $CUTS

mkdir -p $OUT/clip2
ffmpeg -nostdin -v error -y -f concat -safe 0 -i $TMP/list.txt -i $TMP/music.wav \
  -filter_complex "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.84:level=false[a]" \
  -map 0:v -map "[a]" \
  -c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -r 25 -movflags +faststart \
  -c:a aac -b:a 192k -ar 48000 -t $TOTAL \
  $OUT/clip2/MATSU_Clip2_FOMO_9x16.mp4
rm -rf $TMP
echo done
