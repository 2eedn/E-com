import { useState } from 'react'
import { useCart } from '../store/cart'
import { postJSON } from '../api'

export default function Checkout(){
  const { items, inc, dec, remove, clear } = useCart()
  const [email, setEmail] = useState('')
  const [name, setName] = useState('')
  const [result, setResult] = useState(null)
  const total = items.reduce((s,i)=>s + i.product.price_cents * i.qty, 0)

  async function submit(){
    if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return alert('Email tidak valid')
    if(!name) return alert('Nama wajib')
    if(!items.length) return alert('Cart kosong')
    const payload = { email, name, items: items.map(i=>({ product_id: i.product.id, qty: i.qty })) }
    try{
      const r = await postJSON('/orders/checkout/guest', payload)
      setResult(r)
      clear()
    }catch(e){ alert('Gagal membuat pesanan') }
  }

  if(result) return <div className='max-w-2xl mx-auto p-4'>Terima kasih! Kode: <b>{result.order_code}</b></div>

  return (
    <div className='max-w-3xl mx-auto p-4 grid gap-4 md:grid-cols-2'>
      <div className='border rounded-2xl p-4'>
        <h2 className='font-semibold mb-2'>Keranjang</h2>
        {!items.length && <p>Keranjang kosong.</p>}
        {items.map(i=>(
          <div key={i.product.id} className='flex items-center justify-between py-2'>
            <div><div className='font-medium'>{i.product.name}</div><div className='text-sm text-gray-600'>Rp {i.product.price_cents.toLocaleString()}</div></div>
            <div className='flex items-center gap-2'>
              <button onClick={()=>dec(i.product.id)} className='px-2 border rounded'>-</button>
              <span>{i.qty}</span>
              <button onClick={()=>inc(i.product.id)} className='px-2 border rounded'>+</button>
              <button onClick={()=>remove(i.product.id)} className='px-2 border rounded'>Hapus</button>
            </div>
          </div>
        ))}
        <div className='mt-2 font-bold flex justify-between'><span>Total</span><span>Rp {total.toLocaleString()}</span></div>
      </div>
      <div className='border rounded-2xl p-4'>
        <h2 className='font-semibold mb-2'>Checkout (Guest)</h2>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder='Nama' className='border rounded-xl p-2 w-full mb-2'/>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder='Email' className='border rounded-xl p-2 w-full mb-2'/>
        <button onClick={submit} className='w-full rounded-xl bg-black text-white py-2'>Buat Pesanan</button>
      </div>
    </div>
  )
}
