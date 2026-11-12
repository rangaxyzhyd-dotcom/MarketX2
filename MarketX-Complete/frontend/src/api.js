const BASE=import.meta.env.VITE_API_URL||'http://127.0.0.1:8000';
export function token(){return localStorage.getItem('marketx_token')}
export async function api(path,opts={}){const headers={...(opts.body instanceof FormData?{}:{'Content-Type':'application/json'}),...(opts.headers||{})};if(token())headers.Authorization=`Bearer ${token()}`;const res=await fetch(BASE+path,{...opts,headers});if(!res.ok){let msg='Something went wrong';try{const d=await res.json();msg=d.detail||msg}catch{}throw new Error(msg)}if(res.status===204)return null;return res.json()}
export const img=(url)=>url?.startsWith('http')?url:url?BASE+url:'';
export {BASE};
