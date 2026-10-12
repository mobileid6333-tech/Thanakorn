import SummaryDashboard from "@/components/SummaryDashboard";

export default function SummaryPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-primary">สรุปยอด</h1>
        <p className="mt-1 text-muted">
          ภาพรวมยอดขาย สถานะคำสั่งซื้อ และยอดที่ร้านค้ายังไม่ชำระ
        </p>
      </div>
      <SummaryDashboard />
    </div>
  );
}
