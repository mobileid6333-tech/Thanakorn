# คลิปที่ 1: MATSU HAND ROLL TACO ที่งาน WAMM MARKET FEST ขอนแก่น ยาว 30 วินาที
# วิธีใช้: python3 render1.py   (ส่วนปรับภาพ/ข้อความ/เพลงอยู่ใน engine.py)
import os
from engine import build, YELLOW, WHITE, HERE

END = ('panel', [('MATSU HAND ROLL TACO', 76, WHITE, True), '---',
                 ('WAMM MARKET FEST', 60, YELLOW, True),
                 ('6–8 NOV  |  CENTRAL KHON KAEN', 44, WHITE, False)])
# (ที่มา, เริ่ม, ยาว, ซูม, ข้อความ)
SHOTS = [
    # 0–5 Opening Hook
    ('08269', 0.0, 1.5, 0.025, None),
    ('IMG@300', 0, 1.0, 0.04, None),
    ('07864', 1.0, 1.0, 0.025, None),
    ('07756', 0.0, 1.5, 0.03, None),
    # 5–15 Chef & Food
    ('07626', 2.0, 1.5, 0.03, None),
    ('07629', 3.5, 1.0, 0.03, None),
    ('07633', 3.5, 1.0, 0.03, None),
    ('07648', 0.0, 1.0, 0.03, None),
    ('07647', 1.0, 1.0, 0.03, None),
    ('07753', 1.5, 2.0, 0.03, None),
    ('07875', 0.0, 1.5, 0.03, None),
    ('07755', 2.0, 1.0, 0.03, None),
    # 15–23 Event Vibe (เริ่มด้วยภาพหน้าบูธ)
    ('07879', 1.7, 1.5, 0.025, None),
    ('07872', 1.5, 1.0, 0.025, None),
    ('07866', 2.0, 2.0, 0.025, None),
    ('07877', 0.3, 1.5, 0.025, None),
    ('07878', 3.0, 1.0, 0.025, None),
    ('07879', 6.0, 1.0, 0.025, None),
    # 23–30 Ending
    ('IMG@750', 0, 2.5, 0.06, None),
    ('08269', 2.5, 4.5, 0.025, END),
]
build(SHOTS, os.path.join(HERE, 'MATSU_HandRollTaco_9x16.mp4'), '5,15', 'parts1')
