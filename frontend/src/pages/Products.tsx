import { useEffect, useState, useMemo } from 'react'
import ProductCard from '../components/ProductCard'
import { fetchJSON } from '../api'
import { useCart } from '../store/cart'

export default function Products(){
  const [data, setData] = useState([])
  const [q, setQ] = useState('')
  const [page, setPage] = useState(1)
  const [pageSize, setPageSize] = useState(12)
  const cartAdd = useCart(s=>s.add)

  const query = useMemo(()=>{
    const u = new URLSearchParams()
    if(q) u.set('q', q)
    u.set('page', String(page))
    u.set('page_size', String(pageSize))
    return `/products?${u.toString()}`
  }, [q, page, pageSize])

  useEffect(()=>{
    const t = setTimeout(()=> {
      fetchJSON(query).then(r=> setData(r.data)).catch(()=>{})
    }, 250)
    return ()=>clearTimeout(t)
  }, [query])

  return (
    <div className='max-w-6xl mx-auto p-4'>
      <h1 className='text-2xl font-bold mb-4'>Produk</h1>
      <div className='grid gap-3 md:grid-cols-4 mb-4'>
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder='Cari...' className='border rounded-xl p-2'/>
        <select onChange={e=>setPageSize(Number(e.target.value))} className='border rounded-xl p-2'>
          <option value={8}>8</option><option value={12}>12</option><option value={24}>24</option>
        </select>
      </div>
      <div className='grid gap-4 grid-cols-2 md:grid-cols-3 lg:grid-cols-4'>
        {data.map(p => <ProductCard key={p.id} p={p} onAdd={cartAdd}/>)}
      </div>
      <div className='mt-6 flex items-center justify-center gap-2'>
        <button onClick={()=>setPage(p => Math.max(1, p-1))} className='px-3 py-1 border rounded-xl'>Prev</button>
        <span>Hal {page}</span>
        <button onClick={()=>setPage(p=>p+1)} className='px-3 py-1 border rounded-xl'>Next</button>
      </div>
    </div>
  )
}
