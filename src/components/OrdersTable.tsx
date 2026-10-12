"use client";

import { useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import StatusBadge from "@/components/StatusBadge";
import { listOrders, updateOrderStatus } from "@/lib/order-store";
import {
  ORDER_STATUSES,
  OVERDUE_DAYS,
  STATUS_LABELS,
  daysSince,
  formatBaht,
  formatThaiDate,
  isOverdue,
  orderTotal,
  type Order,
  type OrderStatus,
} from "@/lib/orders";

type Filter = "all" | OrderStatus | "overdue";

const FILTERS: { value: Filter; label: string }[] = [
  { value: "all", label: "ทั้งหมด" },
  ...ORDER_STATUSES.map((status) => ({
    value: status,
    label: STATUS_LABELS[status],
  })),
  { value: "overdue", label: `ค้างเกิน ${OVERDUE_DAYS} วัน` },
];

function matchesFilter(order: Order, filter: Filter): boolean {
  if (filter === "all") return true;
  if (filter === "overdue") return isOverdue(order);
  return order.status === filter;
}

export default function OrdersTable() {
  const [orders, setOrders] = useState<Order[] | null>(null);
  const [filter, setFilter] = useState<Filter>("all");
  const [search, setSearch] = useState("");
  const addedNo = useSearchParams().get("added");

  useEffect(() => {
    listOrders().then(setOrders);
  }, []);

  const visible = useMemo(() => {
    const keyword = search.trim();
    return (orders ?? []).filter(
      (order) =>
        matchesFilter(order, filter) &&
        (keyword === "" || order.shopName.includes(keyword)),
    );
  }, [orders, filter, search]);

  async function changeStatus(id: string, status: OrderStatus) {
    await updateOrderStatus(id, status);
    setOrders(await listOrders());
  }

  if (orders === null) {
    return <p className="text-muted">กำลังโหลดข้อมูล...</p>;
  }

  const added = orders.find((order) => order.orderNo === addedNo);

  return (
    <div className="space-y-4">
      {added && (
        <div
          role="status"
          className="rounded-lg border border-emerald-200 bg-emerald-50 px-4 py-3 text-emerald-800"
        >
          บันทึกคำสั่งซื้อเลขที่ {added.orderNo} ของ{added.shopName} เรียบร้อยแล้ว
          ยอดเงิน {formatBaht(orderTotal(added))}
        </div>
      )}
      <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
        <div className="flex flex-wrap gap-2" role="group" aria-label="กรองตามสถานะ">
          {FILTERS.map((option) => (
            <button
              key={option.value}
              type="button"
              onClick={() => setFilter(option.value)}
              aria-pressed={filter === option.value}
              className={`rounded-md border px-3 py-1.5 text-base ${
                filter === option.value
                  ? "border-primary bg-primary text-white"
                  : "border-border bg-surface hover:bg-primary-soft"
              }`}
            >
              {option.label}
            </button>
          ))}
        </div>
        <label className="flex items-center gap-2">
          <span className="whitespace-nowrap text-base">ค้นหาร้าน</span>
          <input
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            placeholder="พิมพ์ชื่อร้าน"
            className="w-full rounded-md border border-border bg-surface px-3 py-1.5 md:w-56"
          />
        </label>
      </div>

      <p className="text-base text-muted">
        แสดง {visible.length} จาก {orders.length} รายการ
      </p>

      {visible.length === 0 ? (
        <p className="rounded-lg border border-border bg-surface px-4 py-10 text-center text-muted">
          ไม่พบคำสั่งซื้อที่ตรงกับเงื่อนไข
        </p>
      ) : (
        <>
          <div className="hidden overflow-x-auto rounded-lg border border-border bg-surface lg:block">
            <table className="w-full text-left text-base">
              <thead className="border-b border-border bg-primary-soft text-sm text-primary">
                <tr>
                  <th className="px-3 py-3 font-semibold">เลขที่</th>
                  <th className="px-3 py-3 font-semibold">ร้าน</th>
                  <th className="px-3 py-3 font-semibold">หนังสือ</th>
                  <th className="whitespace-nowrap px-3 py-3 text-right font-semibold">
                    จำนวน (เล่ม)
                  </th>
                  <th className="px-3 py-3 text-right font-semibold">ยอดเงิน</th>
                  <th className="px-3 py-3 font-semibold">วันที่สั่ง</th>
                  <th className="px-3 py-3 font-semibold">สถานะ</th>
                  <th className="whitespace-nowrap px-3 py-3 font-semibold">
                    เปลี่ยนสถานะ
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border">
                {visible.map((order) => (
                  <tr
                    key={order.id}
                    className={`align-top ${rowTone(order, addedNo)}`}
                  >
                    <td className="whitespace-nowrap px-3 py-3 font-medium">
                      {order.orderNo}
                    </td>
                    <td className="whitespace-nowrap px-3 py-3">{order.shopName}</td>
                    <td className="px-3 py-3">
                      <ul>
                        {order.items.map((item, index) => (
                          <li key={index} className="whitespace-nowrap">
                            {item.title}
                          </li>
                        ))}
                      </ul>
                    </td>
                    <td className="px-3 py-3 text-right tabular-nums">
                      <ul>
                        {order.items.map((item, index) => (
                          <li key={index}>{item.quantity.toLocaleString("th-TH")}</li>
                        ))}
                      </ul>
                    </td>
                    <td className="whitespace-nowrap px-3 py-3 text-right font-medium tabular-nums">
                      {formatBaht(orderTotal(order))}
                    </td>
                    <td className="whitespace-nowrap px-3 py-3">
                      {formatThaiDate(order.orderDate)}
                    </td>
                    <td className="px-3 py-3">
                      <StatusBadge status={order.status} />
                      <OverdueNote order={order} />
                    </td>
                    <td className="px-3 py-3">
                      <AdvanceStatusButton order={order} onChange={changeStatus} />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <ul className="space-y-3 lg:hidden">
            {visible.map((order) => (
              <li
                key={order.id}
                className={`rounded-lg border p-4 ${cardTone(order, addedNo)}`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <p className="text-sm text-muted">
                      {order.orderNo} · {formatThaiDate(order.orderDate)}
                    </p>
                    <p className="font-semibold">{order.shopName}</p>
                  </div>
                  <div className="text-right">
                    <StatusBadge status={order.status} />
                    <OverdueNote order={order} />
                  </div>
                </div>
                <ul className="mt-3 space-y-1 border-t border-border pt-3">
                  {order.items.map((item, index) => (
                    <li key={index} className="flex justify-between gap-3">
                      <span>{item.title}</span>
                      <span className="whitespace-nowrap tabular-nums text-muted">
                        {item.quantity.toLocaleString("th-TH")} เล่ม
                      </span>
                    </li>
                  ))}
                </ul>
                <div className="mt-3 flex items-center justify-between gap-3 border-t border-border pt-3">
                  <AdvanceStatusButton order={order} onChange={changeStatus} />
                  <span className="text-lg font-semibold tabular-nums">
                    {formatBaht(orderTotal(order))}
                  </span>
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}

function OverdueNote({ order }: { order: Order }) {
  if (!isOverdue(order)) return null;
  return (
    <p className="mt-1 whitespace-nowrap text-sm font-medium text-red-700">
      ค้าง {daysSince(order.orderDate)} วัน
    </p>
  );
}

function rowTone(order: Order, addedNo: string | null) {
  if (isOverdue(order)) return "bg-red-50 shadow-[inset_4px_0_0_0_#b91c1c]";
  if (order.orderNo === addedNo) return "bg-emerald-50";
  return "";
}

function cardTone(order: Order, addedNo: string | null) {
  if (isOverdue(order)) return "border-red-300 border-l-4 border-l-red-700 bg-red-50";
  if (order.orderNo === addedNo) return "border-emerald-300 bg-emerald-50";
  return "border-border bg-surface";
}

const NEXT_STATUS: Partial<Record<OrderStatus, OrderStatus>> = {
  pending: "shipped",
  shipped: "paid",
};

function AdvanceStatusButton({
  order,
  onChange,
}: {
  order: Order;
  onChange: (id: string, status: OrderStatus) => void;
}) {
  const next = NEXT_STATUS[order.status];
  if (!next) {
    return <span className="whitespace-nowrap text-base text-muted">เสร็จสิ้น</span>;
  }
  return (
    <button
      type="button"
      onClick={() => onChange(order.id, next)}
      aria-label={`เปลี่ยนสถานะ ${order.orderNo} เป็น${STATUS_LABELS[next]}`}
      className="whitespace-nowrap rounded-md border border-primary bg-surface px-3 py-1 text-base text-primary hover:bg-primary-soft"
    >
      เป็น{STATUS_LABELS[next]} &rarr;
    </button>
  );
}
