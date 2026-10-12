// จุดเดียวที่อ่านและบันทึกข้อมูลคำสั่งซื้อ
// รอบนี้เก็บในเบราว์เซอร์ (localStorage) ช่วงบ่ายจะเปลี่ยนไฟล์นี้ไปเรียก Supabase
// ทุกฟังก์ชันคืนค่าเป็น Promise อยู่แล้ว หน้าเว็บจึงไม่ต้องแก้ตอนเปลี่ยน

import type { Order, OrderStatus } from "./orders";
import { createSampleOrders } from "./sample-orders";

const STORAGE_KEY = "amata-orders-v1";

function readAll(): Order[] {
  const saved = window.localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      return JSON.parse(saved) as Order[];
    } catch {
      // ข้อมูลเสีย ให้เริ่มจากข้อมูลตัวอย่างใหม่
    }
  }
  const sample = createSampleOrders();
  writeAll(sample);
  return sample;
}

function writeAll(orders: Order[]) {
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(orders));
}

export async function listOrders(): Promise<Order[]> {
  return readAll().sort(
    (a, b) =>
      b.orderDate.localeCompare(a.orderDate) ||
      b.orderNo.localeCompare(a.orderNo),
  );
}

export async function updateOrderStatus(
  id: string,
  status: OrderStatus,
): Promise<void> {
  writeAll(
    readAll().map((order) => (order.id === id ? { ...order, status } : order)),
  );
}
