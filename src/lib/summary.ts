import {
  ORDER_STATUSES,
  isOverdue,
  orderTotal,
  type Order,
  type OrderStatus,
} from "./orders";

export type ShopTotal = {
  shopName: string;
  total: number;
  paid: number;
  outstanding: number;
  orderCount: number;
};

export type Summary = {
  totalSales: number;
  orderCount: number;
  byStatus: Record<OrderStatus, { count: number; amount: number }>;
  outstanding: number;
  outstandingCount: number;
  overdueAmount: number;
  overdueCount: number;
  topShops: ShopTotal[];
};

export function summarize(orders: Order[], topN = 5): Summary {
  const byStatus = Object.fromEntries(
    ORDER_STATUSES.map((status) => [status, { count: 0, amount: 0 }]),
  ) as Summary["byStatus"];
  const shops = new Map<string, ShopTotal>();
  let totalSales = 0;
  let overdueAmount = 0;
  let overdueCount = 0;

  for (const order of orders) {
    const amount = orderTotal(order);
    totalSales += amount;
    byStatus[order.status].count += 1;
    byStatus[order.status].amount += amount;
    if (isOverdue(order)) {
      overdueAmount += amount;
      overdueCount += 1;
    }

    const shop = shops.get(order.shopName) ?? {
      shopName: order.shopName,
      total: 0,
      paid: 0,
      outstanding: 0,
      orderCount: 0,
    };
    shop.total += amount;
    shop.orderCount += 1;
    if (order.status === "paid") shop.paid += amount;
    else shop.outstanding += amount;
    shops.set(order.shopName, shop);
  }

  return {
    totalSales,
    orderCount: orders.length,
    byStatus,
    outstanding: byStatus.pending.amount + byStatus.shipped.amount,
    outstandingCount: byStatus.pending.count + byStatus.shipped.count,
    overdueAmount,
    overdueCount,
    topShops: [...shops.values()]
      .sort((a, b) => b.total - a.total)
      .slice(0, topN),
  };
}
