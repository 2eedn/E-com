const API = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'
export async function fetchJSON(url){
  const res = await fetch(API + url)
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}
export async function postJSON(url, body){
  const res = await fetch(API + url, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(body)})
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}
