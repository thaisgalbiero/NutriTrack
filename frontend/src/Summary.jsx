import React, {useEffect, useState} from 'react';
const fields = [['calories','Calorias','kcal'],['protein','Proteínas','g'],['carbs','Carboidratos','g'],['fat','Gorduras','g']];
const empty = {calories:'',protein:'',carbs:'',fat:''};
const today = () => {const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`};
const fmt = v => Number(v).toLocaleString('pt-BR',{maximumFractionDigits:1});
export default function Summary({api,onExpired}) {
 const [date,setDate]=useState(today),[data,setData]=useState(null),[goals,setGoals]=useState(empty);
 const [error,setError]=useState(''),[notice,setNotice]=useState(''),[busy,setBusy]=useState(false),[refresh,setRefresh]=useState(0);
 function fail(e){setError(e.message);if([401,403].includes(e.status))onExpired()}
 useEffect(()=>{let active=true;setData(null);setError('');api(`/dashboard?date=${date}`).then(d=>{if(active)setData(d)}).catch(e=>{if(active)fail(e)});return()=>{active=false}},[date,refresh]);
 useEffect(()=>{let active=true;api('/goals').then(g=>{if(active)setGoals(g||empty)}).catch(e=>{if(active)fail(e)});return()=>{active=false}},[]);
 async function save(e){e.preventDefault();setBusy(true);setError('');setNotice('');try{await api('/goals',{method:'PUT',body:JSON.stringify(Object.fromEntries(fields.map(([k])=>[k,Number(goals[k])]))) });setRefresh(v=>v+1);setNotice('Metas salvas.')}catch(e){fail(e)}finally{setBusy(false)}}
 return <>
 <div className="diary-toolbar"><div><span className="eyebrow">ACOMPANHAMENTO NUTRICIONAL</span><h2>Seu dia em números.</h2></div><label className="date-filter">Data do resumo<input type="date" value={date} disabled={busy} onChange={e=>{if(e.target.value)setDate(e.target.value)}}/></label></div>
 {error&&<p role="alert" className="message error">{error}</p>}{notice&&<p role="status" className="message success">{notice}</p>}
 {data?<><p className="muted">{data.meal_count} refeição(ões) registrada(s) nesta data.</p><div className="nutrition-stats">{fields.map(([k,label,unit])=><section className="card nutrient" key={k}><span>{label}</span><h2>{fmt(data.totals[k])} <small>{unit}</small></h2>{data.goals?<><progress aria-label={`${label}: progresso da meta`} max="100" value={Math.min(100,data.progress[k])}/><p>{fmt(data.progress[k])}% de {fmt(data.goals[k])} {unit}</p>{data.progress[k]>100&&<span>Meta ultrapassada</span>}</>:<p className="muted">Meta ainda não definida.</p>}</section>)}</div>{!data.meal_count&&<p className="empty">Registre uma refeição em “Minhas refeições” para acompanhar os totais.</p>}</>:!error&&<p role="status">Carregando resumo…</p>}
 <section className="card goals"><h2>Minhas metas diárias</h2><p className="muted">Informe seus valores de referência. As metas atuais são usadas na comparação de qualquer data.</p><form onSubmit={save}><fieldset disabled={busy}><div className="two">{fields.map(([k,label,unit])=><label key={k}>{label} ({unit})<input type="number" min="0.1" max={k==='calories'?20000:2000} step="0.1" required value={goals[k]} onChange={e=>setGoals({...goals,[k]:e.target.value})}/></label>)}</div><button>{busy?'Salvando…':'Salvar metas'}</button></fieldset></form></section>
 <p className="muted">Cálculo: valor nutricional por 100 g × quantidade consumida ÷ 100. As calorias usam o valor cadastrado do alimento.</p>
 </>;
}
