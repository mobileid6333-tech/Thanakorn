"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import StatusBadge from "@/components/StatusBadge";
import { listOrders } from "@/lib/order-store";
import {
  ORDER_STATUSES,
  OVERDUE_DAYS,
  formatBaht,
  type Order,
} from "@/lib/orders";
import { summarize, type ShopTotal } from "@/lib/summary";

export default function SummaryDashboard() {
  const [orders, setOrders] = useState<Order[] | null>(null);

  useEffect(() => {
    listOrders().then(setOrders);
  }, []);

  if (orders === null) {
    return <p className="text-muted">กำลังโหลดข้อมูล...</p>;
  }

  const summary = summarize(orders);

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-border bg-surface p-5">
          <h2 className="text-base font-medium text-muted">ยอดขายรวม</h2>
          <p className="mt-1 text-5xl font-bold text-primary">
            {formatBaht(summary.totalSales)}
          </p>
          <p className="mt-2 text-base text-muted">
            จากคำสั่งซื้อทั้งหมด {summary.orderCount} ใบ
          </p>
        </div>
        <div className="rounded-lg border border-border bg-surface p-5">
          <h2 className="text-base font-medium text-muted">ยอดค้างชำระรวม</h2>
          <p className="mt-1 text-4xl font-bold">
            {formatBaht(summary.outstanding)}
          </p>
          <p className="mt-2 text-base text-muted">
            {summary.outstandingCount} ใบที่ยังไม่ชำระ (รอส่งและส่งแล้ว)
          </p>
          {summary.overdueCount > 0 && (
            <Link
              href="/orders?filter=overdue"
              className="mt-3 inline-block rounded-md bg-red-50 px-3 py-1.5 text-base font-medium text-red-800 ring-1 ring-inset ring-red-200 hover:bg-red-100"
            >
              ค้างเกิน {OVERDUE_DAYS} วัน {summary.overdueCount} ใบ รวม{" "}
              {formatBaht(summary.overdueAmount)}
            </Link>
          )}
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold">จำนวนคำสั่งซื้อแยกตามสถานะ</h2>
        <div className="grid gap-4 sm:grid-cols-3">
          {ORDER_STATUSES.map((status) => (
            <div
              key={status}
              className="rounded-lg border border-border bg-surface p-5"
            >
              <StatusBadge status={status} />
              <p className="mt-3 text-4xl font-bold">
                {summary.byStatus[status].count}
                <span className="ml-2 text-lg font-normal text-muted">ใบ</span>
              </p>
              <p className="mt-1 text-base text-muted">
                มูลค่า {formatBaht(summary.byStatus[status].amount)}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface p-5">
        <h2 className="text-lg font-semibold">
          ร้านที่ยอดสั่งซื้อสูงสุด {summary.topShops.length} อันดับ
        </h2>
        <p className="mt-1 text-base text-muted">
          ยอดรวมทุกสถานะ ชี้หรือแตะที่แท่งเพื่อดูยอดชำระแล้วและยอดค้าง
        </p>
        <TopShopsChart shops={summary.topShops} />
      </section>
    </div>
  );
}

function TopShopsChart({ shops }: { shops: ShopTotal[] }) {
  const [active, setActive] = useState<string | null>(null);
  const max = Math.max(1, ...shops.map((shop) => shop.total));

  if (shops.length === 0) {
    return <p className="mt-4 text-muted">ยังไม่มีข้อมูล</p>;
  }

  return (
    <ol className="mt-5 space-y-4" aria-label="ร้านที่ยอดสั่งซื้อสูงสุด">
      {shops.map((shop, index) => {
        const isActive = active === shop.shopName;
        return (
          <li
            key={shop.shopName}
            className="relative grid gap-1 rounded-md outline-none sm:grid-cols-[14rem_1fr] sm:items-center sm:gap-4"
            tabIndex={0}
            onMouseEnter={() => setActive(shop.shopName)}
            onMouseLeave={() => setActive(null)}
            onFocus={() => setActive(shop.shopName)}
            onBlur={() => setActive(null)}
            onClick={() => setActive(isActive ? null : shop.shopName)}
          >
            <span className="text-base">
              <span className="mr-2 text-muted">{index + 1}.</span>
              {shop.shopName}
            </span>
            <span className="flex items-center gap-3 py-1">
              <span
                className={`h-6 rounded-r transition-opacity ${
                  active && !isActive ? "opacity-40" : ""
                }`}
                style={{
                  width: `${(shop.total / max) * 75}%`,
                  backgroundColor: "var(--primary)",
                }}
              />
              <span className="whitespace-nowrap text-base font-semibold">
                {formatBaht(shop.total)}
              </span>
            </span>
            {isActive && (
              <span
                role="tooltip"
                className="absolute right-0 top-full z-10 mt-1 w-64 rounded-md border border-border bg-surface p-3 text-sm shadow-md sm:left-56 sm:right-auto"
              >
                <span className="block font-semibold">{shop.shopName}</span>
                <span className="mt-1 flex justify-between">
                  <span className="text-muted">คำสั่งซื้อ</span>
                  <span>{shop.orderCount} ใบ</span>
                </span>
                <span className="flex justify-between">
                  <span className="text-muted">ชำระแล้ว</span>
                  <span>{formatBaht(shop.paid)}</span>
                </span>
                <span className="flex justify-between">
                  <span className="text-muted">ยังไม่ชำระ</span>
                  <span>{formatBaht(shop.outstanding)}</span>
                </span>
              </span>
            )}
          </li>
        );
      })}
    </ol>
  );
}
