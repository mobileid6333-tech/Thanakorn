import Link from "next/link";
import OrdersTable from "@/components/OrdersTable";

export default function OrdersPage() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-bold text-primary">รายการคำสั่งซื้อ</h1>
          <p className="mt-1 text-muted">
            คำสั่งซื้อทั้งหมดจากร้านค้า เรียงจากล่าสุด
          </p>
        </div>
        <Link
          href="/orders/new"
          className="self-start rounded-md bg-primary px-4 py-2 text-white sm:self-auto"
        >
          เพิ่มคำสั่งซื้อ
        </Link>
      </div>
      <OrdersTable />
    </div>
  );
}
