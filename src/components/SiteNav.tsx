"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { PUBLISHER_NAME, SYSTEM_NAME } from "@/lib/site";

const links = [
  { href: "/", label: "หน้าแรก" },
  { href: "/orders", label: "รายการคำสั่งซื้อ" },
  { href: "/orders/new", label: "เพิ่มคำสั่งซื้อ" },
  { href: "/summary", label: "สรุปยอด" },
];

export default function SiteNav() {
  const pathname = usePathname();

  return (
    <header className="border-b border-border bg-surface">
      <div className="mx-auto flex max-w-6xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <Link href="/" className="leading-tight">
          <span className="block text-2xl font-bold text-primary">
            {SYSTEM_NAME}
          </span>
          <span className="block text-sm text-muted">
            ระบบติดตามคำสั่งซื้อหนังสือ {PUBLISHER_NAME}
          </span>
        </Link>
        <nav className="flex flex-wrap gap-1">
          {links.map((link) => {
            const active = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                aria-current={active ? "page" : undefined}
                className={`rounded-md px-3 py-2 text-base font-medium ${
                  active
                    ? "bg-primary text-white"
                    : "text-foreground hover:bg-primary-soft"
                }`}
              >
                {link.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
