import type { Metadata } from "next";
import { Sarabun } from "next/font/google";
import SiteNav from "@/components/SiteNav";
import { PUBLISHER_NAME, SYSTEM_NAME } from "@/lib/site";
import "./globals.css";

const sarabun = Sarabun({
  variable: "--font-sarabun",
  subsets: ["thai", "latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: `${SYSTEM_NAME} | ระบบติดตามคำสั่งซื้อ ${PUBLISHER_NAME}`,
  description: "ระบบติดตามคำสั่งซื้อหนังสือจากร้านค้า สำนักพิมพ์อมตะ",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="th" className={`${sarabun.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col font-sans">
        <SiteNav />
        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6">
          {children}
        </main>
        <footer className="border-t border-border bg-surface">
          <div className="mx-auto max-w-6xl px-4 py-4 text-sm text-muted sm:px-6">
            สำนักพิมพ์อมตะ ระบบติดตามคำสั่งซื้อหนังสือ
          </div>
        </footer>
      </body>
    </html>
  );
}
