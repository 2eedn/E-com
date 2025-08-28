import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Products from './pages/Products'
import Checkout from './pages/Checkout'
import Orders from './pages/Orders'
export default function App(){
  return (
    <BrowserRouter>
      <header className='sticky top-0 z-10 bg-white border-b'>
        <nav className='max-w-6xl mx-auto p-3 flex items-center justify-between'>
          <Link to='/'>SimpleShop</Link>
          <div className='flex items-center gap-4'>
            <Link to='/orders'>Pesanan</Link>
            <Link to='/checkout'>Checkout</Link>
          </div>
        </nav>
      </header>
      <Routes>
        <Route path='/' element={<Products/>}/>
        <Route path='/checkout' element={<Checkout/>}/>
        <Route path='/orders' element={<Orders/>}/>
      </Routes>
    </BrowserRouter>
  )
}
