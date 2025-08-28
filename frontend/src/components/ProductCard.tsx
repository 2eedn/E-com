export default function ProductCard({p, onAdd}) {
  return (
    <div className='rounded-2xl shadow p-4 flex flex-col'>
      <img loading='lazy' src={p.image_url} alt={p.name} className='w-full h-40 object-cover rounded-xl'/>
      <h3 className='mt-2 font-semibold'>{p.name}</h3>
      <p className='text-sm text-gray-600'>{p.description}</p>
      <div className='mt-auto flex items-center justify-between'>
        <span className='font-bold'>Rp {p.price_cents.toLocaleString()}</span>
        <button onClick={()=>onAdd(p)} className='px-3 py-1 rounded-xl bg-black text-white'>Tambah</button>
      </div>
    </div>
  )
}
