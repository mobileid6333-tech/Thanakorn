import Link from "next/link";

export default function ComingSoon({
  title,
  step,
}: {
  title: string;
  step: number;
}) {
  return (
    <div className="rounded-lg border border-border bg-surface p-8">
      <h1 className="text-2xl font-bold text-primary">{title}</h1>
      <p className="mt-3 text-muted">
        หน้านี้กำลังจัดทำ จะเปิดใช้งานในขั้นที่ {step}
      </p>
      <Link
        href="/"
        className="mt-6 inline-block rounded-md bg-primary px-4 py-2 text-white"
      >
        กลับหน้าแรก
      </Link>
    </div>
  );
}
