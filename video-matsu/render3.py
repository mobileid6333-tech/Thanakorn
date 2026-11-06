# คลิปที่ 3: "LAST DAY! วันนี้วันสุดท้าย" ขอนแก่น ยาว 19.5 วินาที (ทุกช็อตยาวอย่างน้อย 1 วินาที)
# วิธีใช้: python3 render3.py   (ส่วนปรับภาพ/ข้อความ/เพลงอยู่ใน engine.py)
import os
from engine import build, YELLOW, WHITE, HERE

HOOK = ('label', 'LAST DAY! วันนี้วันสุดท้าย')
CTA = ('label', 'โอกาสสุดท้ายที่จะได้ลอง!')
END = ('panel', [('โอกาสสุดท้ายที่จะได้ลอง!', 64, YELLOW, True), '---',
                 ('MATSU HAND ROLL TACO', 76, WHITE, True),
                 ('8 NOV  |  CENTRAL KHON KAEN', 44, WHITE, False)])
SHOTS = [
    # 0–3 HOOK
    ('IMG@750', 0, 1.0, 0.04, HOOK),
    ('07866', 2.5, 1.0, 0.025, HOOK),
    ('07755', 4.0, 1.0, 0.03, HOOK),
    # 3–8 FOOD & CHEF
    ('07753', 1.5, 1.5, 0.03, None),
    ('ae606221', 0.0, 1.0, 0.03, None),   # เชฟแต่งหน้าแฮนด์โรล (07861)
    ('f2ad9dc6', 0.5, 1.0, 0.03, None),   # เชฟใส่แฮนด์โรลลงกล่อง (07861)
    ('07841', 3.0, 1.5, 0.025, None),
    # 8–14 EVENT MOMENT (เริ่มด้วยภาพหน้าบูธ)
    ('08287', 0.3, 1.5, 0.025, None),   # หน้าบูธตรง ๆ + คิวลูกค้า
    ('07864', 1.0, 1.0, 0.025, None),
    ('07877', 0.3, 1.0, 0.025, None),
    ('07866', 5.0, 1.0, 0.025, None),
    ('07878', 3.0, 1.5, 0.025, None),
    # 14–19.5 FINAL CTA
    ('IMG@pan', 0, 2.5, 0.0, CTA),
    ('07879', 8.0, 3.0, 0.025, END),
]
build(SHOTS, os.path.join(HERE, 'clip3', 'MATSU_Clip3_LastDay_9x16.mp4'), '3,8', 'parts3')
