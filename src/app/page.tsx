import Link from "next/link";

const sections = [
  {
    href: "/orders",
    title: "รายการคำสั่งซื้อ",
    team: "สำหรับฝ่ายธุรการ",
    detail: "ดูคำสั่งซื้อทั้งหมด ค้นหาร้าน และอัปเดตสถานะการจัดส่ง",
  },
  {
    href: "/orders/new",
    title: "เพิ่มคำสั่งซื้อ",
    team: "สำหรับฝ่ายขาย",
    detail: "บันทึกคำสั่งซื้อใหม่จากร้านค้า พร้อมรายการหนังสือและราคา",
  },
  {
    href: "/summary",
    title: "สรุปยอด",
    team: "สำหรับฝ่ายบัญชี",
    detail: "ดูยอดขายรวม และร้านที่ยังไม่ชำระเงิน พร้อมยอดค้างชำระ",
  },
];

export default function Home() {
  return (
    <div className="space-y-8">
      <section>
        <h1 className="text-3xl font-bold text-primary">
          ระบบติดตามคำสั่งซื้อหนังสือ
        </h1>
        <p className="mt-2 text-muted">
          บันทึกคำสั่งซื้อจากร้านค้า ติดตามการจัดส่ง และตรวจสอบการชำระเงิน
          ในที่เดียว เลือกเมนูที่ต้องการด้านล่าง
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {sections.map((section) => (
          <Link
            key={section.href}
            href={section.href}
            className="flex flex-col rounded-lg border border-border bg-surface p-5 transition hover:border-primary hover:shadow-sm"
          >
            <span className="text-sm font-medium text-muted">
              {section.team}
            </span>
            <span className="mt-1 text-xl font-semibold text-primary">
              {section.title}
            </span>
            <span className="mt-2 flex-1 text-base text-foreground">
              {section.detail}
            </span>
            <span className="mt-4 text-base font-medium text-primary">
              เข้าสู่หน้านี้ &rarr;
            </span>
          </Link>
        ))}
      </section>

      <section className="rounded-lg border border-border bg-surface p-5">
        <h2 className="text-lg font-semibold">สถานะคำสั่งซื้อ</h2>
        <ol className="mt-3 flex flex-col items-start gap-2 sm:flex-row sm:items-center sm:gap-3">
          <li className="rounded-md bg-amber-50 px-3 py-1 text-amber-800">
            รอส่ง
          </li>
          <li aria-hidden className="hidden text-muted sm:block">
            &rarr;
          </li>
          <li className="rounded-md bg-sky-50 px-3 py-1 text-sky-800">
            ส่งแล้ว
          </li>
          <li aria-hidden className="hidden text-muted sm:block">
            &rarr;
          </li>
          <li className="rounded-md bg-emerald-50 px-3 py-1 text-emerald-800">
            ชำระแล้ว
          </li>
        </ol>
      </section>
    </div>
  );
}
