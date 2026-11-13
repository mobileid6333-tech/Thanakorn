# คลิป 3: The Beauty of Hamachi — เวอร์ชันแนวนอน 16:9 (1920x1080) ยาว 15 วินาที
# ใช้ฟุตเทจเต็มเฟรมตามที่ถ่ายมา (ไม่หมุน ไม่ตัดขอบ) ลำดับช็อตเดียวกับเวอร์ชันแนวตั้ง render_p03.py
import os
from premium import build, HERE
from render_p03_shots import SHOTS

BRANCH = os.environ.get('BRANCH', 'สาขาขอนแก่น')
OUT = 'ubon' if 'อุบล' in BRANCH else 'khonkaen'
build(SHOTS, os.path.join(HERE, OUT, 'MATSU_03_BeautyOfHamachi_16x9.mp4'), 'parts_p03w',
      slow=1.0, bpm=100, branch=BRANCH, pre='scale=1920:1080,setsar=1', size=(1920, 1080))
