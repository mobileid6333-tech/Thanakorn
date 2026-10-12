// ข้อมูลตัวอย่าง (สมมติทั้งหมด) ชื่อร้านและชื่อหนังสือแต่งขึ้น ไม่ใช่ของจริง
// วันที่คำนวณย้อนหลังจากวันที่เปิดระบบครั้งแรก กระจายประมาณ 2 เดือน

import { daysAgoIso, type Order, type OrderStatus, type OrderItem } from "./orders";

type SampleRow = {
  daysAgo: number;
  shopName: string;
  status: OrderStatus;
  items: OrderItem[];
};

const rows: SampleRow[] = [
  {
    daysAgo: 58,
    shopName: "ร้านหนังสือใบไม้เขียว",
    status: "paid",
    items: [
      { title: "สวนลับหลังบ้านยาย", quantity: 20, unitPrice: 245 },
      { title: "ครัวของแม่ในฤดูฝน", quantity: 10, unitPrice: 320 },
    ],
  },
  {
    daysAgo: 52,
    shopName: "ร้านหนังสือนกกระจิบ",
    status: "shipped",
    items: [
      { title: "แผนที่ของเมืองที่ไม่มีอยู่จริง", quantity: 15, unitPrice: 295 },
    ],
  },
  {
    daysAgo: 47,
    shopName: "ร้านหนังสือเรือนไม้ลำปาง",
    status: "paid",
    items: [
      { title: "บันทึกนักเดินเรือกระดาษ", quantity: 12, unitPrice: 185 },
      { title: "นิทานก่อนนอนของแมวส้ม", quantity: 30, unitPrice: 165 },
    ],
  },
  {
    daysAgo: 41,
    shopName: "ร้านหนังสือต้นมะขามป้อม",
    status: "pending",
    items: [
      { title: "คณิตศาสตร์สำหรับคนกลัวตัวเลข", quantity: 25, unitPrice: 275 },
    ],
  },
  {
    daysAgo: 36,
    shopName: "ร้านหนังสือใบไม้เขียว",
    status: "shipped",
    items: [
      { title: "เสียงระฆังที่วัดร้าง", quantity: 18, unitPrice: 260 },
      { title: "จดหมายถึงตัวเองอีกสิบปี", quantity: 10, unitPrice: 210 },
    ],
  },
  {
    daysAgo: 28,
    shopName: "ร้านอ่านเพลินโคราช",
    status: "paid",
    items: [
      { title: "ครัวของแม่ในฤดูฝน", quantity: 8, unitPrice: 320 },
    ],
  },
  {
    daysAgo: 21,
    shopName: "ร้านสองหน้ากระดาษ",
    status: "shipped",
    items: [
      { title: "นิทานก่อนนอนของแมวส้ม", quantity: 40, unitPrice: 165 },
      { title: "สวนลับหลังบ้านยาย", quantity: 15, unitPrice: 245 },
    ],
  },
  {
    daysAgo: 14,
    shopName: "ร้านหนังสือนกกระจิบ",
    status: "paid",
    items: [
      { title: "จดหมายถึงตัวเองอีกสิบปี", quantity: 20, unitPrice: 210 },
    ],
  },
  {
    daysAgo: 7,
    shopName: "ร้านหนังสือเรือนไม้ลำปาง",
    status: "shipped",
    items: [
      { title: "แผนที่ของเมืองที่ไม่มีอยู่จริง", quantity: 10, unitPrice: 295 },
      { title: "เสียงระฆังที่วัดร้าง", quantity: 10, unitPrice: 260 },
    ],
  },
  {
    daysAgo: 2,
    shopName: "ร้านหนังสือต้นมะขามป้อม",
    status: "pending",
    items: [
      { title: "บันทึกนักเดินเรือกระดาษ", quantity: 24, unitPrice: 185 },
    ],
  },
];

export function createSampleOrders(): Order[] {
  return rows.map((row, index) => {
    const no = String(index + 1).padStart(4, "0");
    return {
      id: `sample-${no}`,
      orderNo: `AMT-${no}`,
      shopName: row.shopName,
      orderDate: daysAgoIso(row.daysAgo),
      status: row.status,
      items: row.items,
    };
  });
}
