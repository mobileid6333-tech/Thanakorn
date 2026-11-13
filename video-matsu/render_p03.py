# คลิป 3: The Beauty of Hamachi — การขึ้นปลาฮามาจิ ยาว 15 วินาที
# ฟุตเทจชุดนี้ถ่ายแนวนอน 25 ภาพ/วินาที: หมุนภาพ 90 องศาให้เป็นแนวตั้งเต็มจอ (ผู้ใช้เลือก) และเล่นความเร็วปกติ
# ฉากจบ: สาขาขอนแก่น (ค่าเริ่มต้น) — ทำเวอร์ชันอุบล: BRANCH=สาขาอุบลราชธานี python3 render_p03.py
import os
from premium import build, HERE

ROTATE = 'scale=1920:1080,setsar=1,transpose=1'   # 1440x1080 (ภาพกว้าง 16:9) → หมุนตามเข็มนาฬิกา → 1080x1920
from render_p03_shots import SHOTS
BRANCH = os.environ.get('BRANCH', 'สาขาขอนแก่น')
OUT = 'ubon' if 'อุบล' in BRANCH else 'khonkaen'
build(SHOTS, os.path.join(HERE, OUT, 'MATSU_03_BeautyOfHamachi.mp4'), 'parts_p03',
      slow=1.0, bpm=100, branch=BRANCH, pre=ROTATE)
