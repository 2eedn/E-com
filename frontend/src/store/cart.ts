import { create } from 'zustand'
export const useCart = create((set)=>({
  items: [],
  add: (p)=> set(s=>{ const found = s.items.find(i=>i.product.id===p.id); if(found){ return { items: s.items.map(i=> i.product.id===p.id?{...i, qty:i.qty+1}:i) } } return { items: [...s.items, { product:p, qty:1 }] } }),
  inc: (id)=> set(s=>({ items: s.items.map(i=> i.product.id===id? {...i, qty:i.qty+1}:i) })),
  dec: (id)=> set(s=>({ items: s.items.map(i=> i.product.id===id? {...i, qty: Math.max(1,i.qty-1)}:i) })),
  remove: (id)=> set(s=>({ items: s.items.filter(i=>i.product.id!==id) })),
  clear: ()=> set({ items: [] })
}))
