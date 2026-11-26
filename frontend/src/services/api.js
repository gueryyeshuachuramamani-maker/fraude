const API=(import.meta.env.VITE_API_URL||"http://127.0.0.1:8000").replace(/\/$/,"");
export async function analizarUrl({url,texto,consent,signal}) {
 const r=await fetch(`${API}/api/analizar`,{method:"POST",headers:{"Content-Type":"application/json","Accept":"application/json"},body:JSON.stringify({url:url.trim(),texto:texto?.trim()||null,autoriza_consulta_externa:Boolean(consent)}),signal});
 let d; try{d=await r.json()}catch{throw new Error("La API no devolvió JSON válido.")};
 if(!r.ok) throw new Error(typeof d.detail==="string"?d.detail:`Error HTTP ${r.status}`);
 return d;
}