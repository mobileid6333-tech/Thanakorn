"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import type { Book } from "@/lib/catalog";
import { addOrder, listBooks, listShops } from "@/lib/order-store";
import { formatBaht, formatThaiDate, todayIso } from "@/lib/orders";

type Row = { key: number; title: string; quantity: string };

type Errors = {
  shop?: string;
  date?: string;
  rows: Record<number, { title?: string; quantity?: string }>;
};

const inputClass =
  "w-full rounded-md border bg-surface px-3 py-2 text-base focus:outline-2 focus:outline-primary";

function fieldClass(hasError: boolean) {
  return `${inputClass} ${hasError ? "border-red-600" : "border-border"}`;
}

function parseQuantity(value: string): number | null {
  const trimmed = value.trim();
  if (!/^\d+$/.test(trimmed)) return null;
  const quantity = Number(trimmed);
  return quantity >= 1 ? quantity : null;
}

function validate(shopName: string, orderDate: string, rows: Row[]): Errors {
  const errors: Errors = { rows: {} };
  if (!shopName) errors.shop = "กรุณาเลือกร้าน";
  if (!orderDate) errors.date = "กรุณาเลือกวันที่สั่ง";
  else if (orderDate > todayIso()) errors.date = "วันที่สั่งต้องไม่เกินวันนี้";

  const seen = new Set<string>();
  for (const row of rows) {
    const rowErrors: { title?: string; quantity?: string } = {};
    if (!row.title) rowErrors.title = "กรุณาเลือกหนังสือ";
    else if (seen.has(row.title))
      rowErrors.title = "เลือกหนังสือเรื่องนี้ซ้ำแล้ว ให้รวมจำนวนไว้แถวเดียว";
    seen.add(row.title);

    if (!row.quantity.trim()) rowErrors.quantity = "กรุณาใส่จำนวน";
    else if (parseQuantity(row.quantity) === null)
      rowErrors.quantity = "จำนวนต้องเป็นตัวเลขจำนวนเต็มตั้งแต่ 1 ขึ้นไป";

    if (rowErrors.title || rowErrors.quantity) errors.rows[row.key] = rowErrors;
  }
  return errors;
}

function hasErrors(errors: Errors) {
  return Boolean(
    errors.shop || errors.date || Object.keys(errors.rows).length > 0,
  );
}

export default function NewOrderForm() {
  const router = useRouter();
  const nextKey = useRef(1);
  const [shops, setShops] = useState<string[] | null>(null);
  const [books, setBooks] = useState<Book[]>([]);
  const [shopName, setShopName] = useState("");
  const [orderDate, setOrderDate] = useState("");
  const [rows, setRows] = useState<Row[]>([{ key: 0, title: "", quantity: "" }]);
  const [submitted, setSubmitted] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    Promise.all([listShops(), listBooks()]).then(([shopList, bookList]) => {
      setShops(shopList);
      setBooks(bookList);
      setOrderDate(todayIso());
    });
  }, []);

  const errors = submitted
    ? validate(shopName, orderDate, rows)
    : { rows: {} as Errors["rows"] };

  function priceOf(title: string) {
    return books.find((book) => book.title === title)?.price ?? 0;
  }

  function lineTotal(row: Row) {
    return (parseQuantity(row.quantity) ?? 0) * priceOf(row.title);
  }

  const grandTotal = rows.reduce((sum, row) => sum + lineTotal(row), 0);

  function updateRow(key: number, change: Partial<Row>) {
    setRows((current) =>
      current.map((row) => (row.key === key ? { ...row, ...change } : row)),
    );
  }

  function addRow() {
    const key = nextKey.current++;
    setRows((current) => [...current, { key, title: "", quantity: "" }]);
  }

  function removeRow(key: number) {
    setRows((current) => current.filter((row) => row.key !== key));
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setSubmitted(true);
    if (hasErrors(validate(shopName, orderDate, rows))) {
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    setSaving(true);
    const order = await addOrder({
      shopName,
      orderDate,
      items: rows.map((row) => ({
        title: row.title,
        quantity: parseQuantity(row.quantity)!,
        unitPrice: priceOf(row.title),
      })),
    });
    router.push(`/orders?added=${encodeURIComponent(order.orderNo)}`);
  }

  if (shops === null) {
    return <p className="text-muted">กำลังโหลดข้อมูล...</p>;
  }

  return (
    <form onSubmit={handleSubmit} noValidate className="space-y-6">
      {hasErrors(errors) && (
        <div
          role="alert"
          className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-red-800"
        >
          กรอกข้อมูลยังไม่ครบหรือไม่ถูกต้อง กรุณาตรวจช่องที่มีข้อความสีแดง
        </div>
      )}

      <section className="grid gap-4 rounded-lg border border-border bg-surface p-5 md:grid-cols-2">
        <div>
          <label htmlFor="shop" className="mb-1 block font-medium">
            ร้าน
          </label>
          <select
            id="shop"
            value={shopName}
            onChange={(event) => setShopName(event.target.value)}
            className={fieldClass(Boolean(errors.shop))}
            aria-invalid={Boolean(errors.shop)}
          >
            <option value="">เลือกร้าน</option>
            {shops.map((shop) => (
              <option key={shop} value={shop}>
                {shop}
              </option>
            ))}
          </select>
          {errors.shop && <ErrorText>{errors.shop}</ErrorText>}
        </div>
        <div>
          <label htmlFor="orderDate" className="mb-1 block font-medium">
            วันที่สั่ง
          </label>
          <input
            id="orderDate"
            type="date"
            value={orderDate}
            max={todayIso()}
            onChange={(event) => setOrderDate(event.target.value)}
            className={fieldClass(Boolean(errors.date))}
            aria-invalid={Boolean(errors.date)}
          />
          {errors.date ? (
            <ErrorText>{errors.date}</ErrorText>
          ) : (
            orderDate && (
              <p className="mt-1 text-sm text-muted">
                ตรงกับวันที่ {formatThaiDate(orderDate)}
              </p>
            )
          )}
        </div>
      </section>

      <section className="rounded-lg border border-border bg-surface p-5">
        <h2 className="text-lg font-semibold">รายการหนังสือ</h2>

        <div className="mt-3 hidden gap-3 border-b border-border pb-2 text-sm font-semibold text-primary md:grid md:grid-cols-[1fr_8rem_8rem_9rem_4rem]">
          <span>หนังสือ</span>
          <span>จำนวน (เล่ม)</span>
          <span className="text-right">ราคาต่อเล่ม</span>
          <span className="text-right">รวม</span>
          <span />
        </div>

        <ul className="divide-y divide-border">
          {rows.map((row, index) => {
            const rowErrors = errors.rows[row.key] ?? {};
            return (
              <li
                key={row.key}
                className="grid gap-3 py-4 md:grid-cols-[1fr_8rem_8rem_9rem_4rem] md:items-start"
              >
                <div>
                  <label
                    htmlFor={`book-${row.key}`}
                    className="mb-1 block text-sm font-medium md:sr-only"
                  >
                    หนังสือเรื่องที่ {index + 1}
                  </label>
                  <select
                    id={`book-${row.key}`}
                    value={row.title}
                    onChange={(event) =>
                      updateRow(row.key, { title: event.target.value })
                    }
                    className={fieldClass(Boolean(rowErrors.title))}
                    aria-invalid={Boolean(rowErrors.title)}
                  >
                    <option value="">เลือกหนังสือ</option>
                    {books.map((book) => (
                      <option key={book.title} value={book.title}>
                        {book.title}
                      </option>
                    ))}
                  </select>
                  {rowErrors.title && <ErrorText>{rowErrors.title}</ErrorText>}
                </div>
                <div>
                  <label
                    htmlFor={`qty-${row.key}`}
                    className="mb-1 block text-sm font-medium md:sr-only"
                  >
                    จำนวน (เล่ม)
                  </label>
                  <input
                    id={`qty-${row.key}`}
                    type="text"
                    inputMode="numeric"
                    value={row.quantity}
                    onChange={(event) =>
                      updateRow(row.key, { quantity: event.target.value })
                    }
                    placeholder="0"
                    className={`${fieldClass(Boolean(rowErrors.quantity))} text-right tabular-nums`}
                    aria-invalid={Boolean(rowErrors.quantity)}
                  />
                  {rowErrors.quantity && (
                    <ErrorText>{rowErrors.quantity}</ErrorText>
                  )}
                </div>
                <div className="flex justify-between md:block md:py-2 md:text-right">
                  <span className="text-sm text-muted md:hidden">ราคาต่อเล่ม</span>
                  <span className="tabular-nums">
                    {row.title ? formatBaht(priceOf(row.title)) : "-"}
                  </span>
                </div>
                <div className="flex justify-between md:block md:py-2 md:text-right">
                  <span className="text-sm text-muted md:hidden">รวม</span>
                  <span className="font-medium tabular-nums">
                    {formatBaht(lineTotal(row))}
                  </span>
                </div>
                <div className="md:py-1 md:text-right">
                  {rows.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeRow(row.key)}
                      className="rounded-md px-2 py-1 text-base text-red-700 hover:bg-red-50"
                      aria-label={`ลบหนังสือเรื่องที่ ${index + 1}`}
                    >
                      ลบ
                    </button>
                  )}
                </div>
              </li>
            );
          })}
        </ul>

        <button
          type="button"
          onClick={addRow}
          className="mt-2 rounded-md border border-primary px-4 py-2 text-primary hover:bg-primary-soft"
        >
          เพิ่มหนังสืออีกเรื่อง
        </button>

        <div className="mt-5 flex items-baseline justify-between border-t border-border pt-4">
          <span className="text-lg font-semibold">ยอดเงินรวม</span>
          <span className="text-2xl font-bold text-primary tabular-nums">
            {formatBaht(grandTotal)}
          </span>
        </div>
      </section>

      <div className="flex flex-wrap gap-3">
        <button
          type="submit"
          disabled={saving}
          className="rounded-md bg-primary px-6 py-2.5 text-white disabled:opacity-60"
        >
          {saving ? "กำลังบันทึก..." : "บันทึกคำสั่งซื้อ"}
        </button>
        <Link
          href="/orders"
          className="rounded-md border border-border bg-surface px-6 py-2.5 hover:bg-primary-soft"
        >
          ยกเลิก
        </Link>
      </div>
    </form>
  );
}

function ErrorText({ children }: { children: React.ReactNode }) {
  return <p className="mt-1 text-sm font-medium text-red-700">{children}</p>;
}
