import NewOrderForm from "@/components/NewOrderForm";

export default function NewOrderPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-primary">เพิ่มคำสั่งซื้อ</h1>
        <p className="mt-1 text-muted">
          เลือกร้านและหนังสือ ใส่จำนวน ระบบจะคิดยอดเงินให้อัตโนมัติ
        </p>
      </div>
      <NewOrderForm />
    </div>
  );
}
