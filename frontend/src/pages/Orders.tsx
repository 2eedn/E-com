import { useState } from 'react'
import { fetchJSON } from '../api'

export default function Orders(){
  const [email, setEmail] = useState('')
  const [code, setCode] = useState('')
  const [data, setData] = useState([])
  const [detail, setDetail] = useState(null)

  async function search(){
    if(!email) return
    const r = await fetchJSON(`/orders?email=${encodeURIComponent(email)}`)
    setData(r.data || [])
  }
  async function loadDetail(){
    if(!code) return
    const r = await fetchJSON(`/orders/${code}`)
    setDetail(r)
  }

  return (
    <div className='max-w-5xl mx-auto p-4'>
      <h1 className='text-2xl font-bold mb-4'>Pesanan</h1>
      <div className='grid md:grid-cols-3 gap-3 mb-4'>
        <input value={email} onChange={e=>setEmail(e.target.value)} placeholder='Cari berdasarkan email' className='border rounded-xl p-2' />
        <input value={code} onChange={e=>setCode(e.target.value)} placeholder='Atau masukkan Kode Pesanan' className='border rounded-xl p-2' />
        <button onClick={loadDetail} className='rounded-xl bg-black text-white px-4'>Lihat Detail</button>
      </div>
      {detail && <div className='border rounded-2xl p-4 mb-4'>Detail: {detail.order_code}</div>}
      <div className='grid gap-2'>
        {data.map(o=>(
          <div key={o.id} className='border rounded-2xl p-3 flex items-center justify-between'>
            <div><div className='font-semibold'>{o.order_code}</div><div className='text-sm text-gray-600'>{o.created_at} — {o.status}</div></div>
            <button onClick={()=>setDetail(o)} className='px-3 py-1 rounded-xl border'>Detail</button>
          </div>
        ))}
      </div>
    </div>
  )
}
