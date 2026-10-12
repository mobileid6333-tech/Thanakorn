// ชนิดข้อมูลและฟังก์ชันช่วยคำนวณ/แสดงผลของคำสั่งซื้อ
// โครงสร้างนี้ตั้งใจให้ตรงกับตารางที่จะสร้างใน Supabase ช่วงบ่าย
// (orders 1 แถวต่อใบ และ order_items 1 แถวต่อหนังสือ 1 เรื่อง)

export const ORDER_STATUSES = ["pending", "shipped", "paid"] as const;
export type OrderStatus = (typeof ORDER_STATUSES)[number];

export const STATUS_LABELS: Record<OrderStatus, string> = {
  pending: "รอส่ง",
  shipped: "ส่งแล้ว",
  paid: "ชำระแล้ว",
};

export type OrderItem = {
  title: string;
  quantity: number;
  unitPrice: number;
};

export type Order = {
  id: string;
  orderNo: string;
  shopName: string;
  // วันที่แบบ ปปปป-ดด-วว (ค.ศ.) เช่น 2026-10-12 ตรงกับชนิด date ของฐานข้อมูล
  orderDate: string;
  status: OrderStatus;
  items: OrderItem[];
};

export const OVERDUE_DAYS = 30;

const TIME_ZONE = "Asia/Bangkok";

export function orderTotal(order: Order): number {
  return order.items.reduce(
    (sum, item) => sum + item.quantity * item.unitPrice,
    0,
  );
}

export function orderQuantity(order: Order): number {
  return order.items.reduce((sum, item) => sum + item.quantity, 0);
}

export function formatBaht(amount: number): string {
  return `฿${amount.toLocaleString("th-TH", {
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  })}`;
}

function parseDate(isoDate: string): Date {
  // ตั้งเวลาเที่ยงวันตามเวลาไทย เพื่อไม่ให้วันที่เลื่อนเพราะเขตเวลา
  return new Date(`${isoDate}T12:00:00+07:00`);
}

export function formatThaiDate(isoDate: string): string {
  return parseDate(isoDate).toLocaleDateString("th-TH", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: TIME_ZONE,
  });
}

export function todayIso(): string {
  // en-CA ให้รูปแบบ ปปปป-ดด-วว
  return new Date().toLocaleDateString("en-CA", { timeZone: TIME_ZONE });
}

export function daysAgoIso(days: number): string {
  const date = parseDate(todayIso());
  date.setUTCDate(date.getUTCDate() - days);
  return date.toLocaleDateString("en-CA", { timeZone: TIME_ZONE });
}

export function daysSince(isoDate: string): number {
  const diff = parseDate(todayIso()).getTime() - parseDate(isoDate).getTime();
  return Math.round(diff / 86_400_000);
}

export function isOverdue(order: Order): boolean {
  return order.status !== "paid" && daysSince(order.orderDate) > OVERDUE_DAYS;
}
