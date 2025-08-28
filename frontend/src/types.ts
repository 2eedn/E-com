export interface Category { id: number; name: string }
export interface Product { id: number; name: string; description?: string; price_cents: number; image_url?: string; category?: Category }
export interface CartItem { product: Product; qty: number }
export interface OrderItemOut { product_id: number; name: string; qty: number; price_cents: number }
export interface OrderOut { id: number; order_code: string; status: string; total_cents: number; created_at: string; items: OrderItemOut[] }
export interface PageMeta { page: number; page_size: number; total: number }
