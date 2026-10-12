import { STATUS_LABELS, type OrderStatus } from "@/lib/orders";

const STYLES: Record<OrderStatus, string> = {
  pending: "bg-amber-50 text-amber-800 ring-amber-200",
  shipped: "bg-sky-50 text-sky-800 ring-sky-200",
  paid: "bg-emerald-50 text-emerald-800 ring-emerald-200",
};

export default function StatusBadge({ status }: { status: OrderStatus }) {
  return (
    <span
      className={`inline-block whitespace-nowrap rounded-full px-3 py-0.5 text-sm font-medium ring-1 ring-inset ${STYLES[status]}`}
    >
      {STATUS_LABELS[status]}
    </span>
  );
}
