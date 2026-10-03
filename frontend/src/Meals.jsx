import React, { useEffect, useRef, useState } from "react";

const types = { breakfast: "Café da manhã", lunch: "Almoço", dinner: "Jantar", snack: "Lanche" };
const icons = { breakfast: "☀", lunch: "◒", dinner: "☾", snack: "♡" };
const today = () => {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}-${String(d.getDate()).padStart(2,"0")}`;
};
const blank = date => ({ date, meal_time: "", meal_type: "breakfast", notes: "", items: [{ food_id: "", quantity_g: "100" }] });

export default function Meals({ foods, api, onExpired }) {
  const [day, setDay] = useState(today);
  const [meals, setMeals] = useState([]);
  const [form, setForm] = useState(() => blank(today()));
  const [editing, setEditing] = useState(null);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [deleting, setDeleting] = useState(null);
  const revision = useRef(0);
  const formRef = useRef(null);

  function fail(err) {
    setError(err.message);
    if (err.status === 401 || err.status === 403) onExpired();
  }
  async function load(date) {
    const current = ++revision.current;
    setLoading(true);
    try {
      const result = await api(`/meals?date=${date}`);
      if (current === revision.current) setMeals(result);
    } catch (err) { if (current === revision.current) fail(err); }
    finally { if (current === revision.current) setLoading(false); }
  }
  useEffect(() => { load(day); return () => { revision.current++; }; }, [day]);
  function reset(date = day) { setEditing(null); setForm(blank(date)); }
  function changeDay(value) {
    if (!value) return;
    setDay(value); reset(value); setDeleting(null); setError(""); setNotice("");
  }
  function itemChange(index, key, value) {
    setForm(prev => ({...prev, items: prev.items.map((item, i) => i === index ? {...item, [key]: value} : item)}));
  }
  async function save(e) {
    e.preventDefault(); setBusy(true); setError(""); setNotice("");
    try {
      const payload = {...form, meal_time: form.meal_time || null, items: form.items.map(i => ({food_id: Number(i.food_id), quantity_g: Number(i.quantity_g)}))};
      await api(editing ? `/meals/${editing}` : "/meals", {method: editing ? "PUT" : "POST", body: JSON.stringify(payload)});
      const target = form.date;
      setNotice(editing ? "Refeição atualizada." : "Refeição registrada com sucesso.");
      reset(target);
      if (target !== day) setDay(target); else await load(day);
    } catch (err) { fail(err); }
    finally { setBusy(false); }
  }
  async function remove(id) {
    setBusy(true); setError(""); setNotice("");
    try {
      await api(`/meals/${id}`, {method: "DELETE"});
      if (editing === id) reset();
      setDeleting(null); setNotice("Refeição excluída."); await load(day);
    } catch (err) { fail(err); }
    finally { setBusy(false); }
  }
  function edit(meal) {
    setEditing(meal.id);
    setForm({date: meal.date, meal_time: meal.meal_time || "", meal_type: meal.meal_type, notes: meal.notes, items: meal.items.map(i => ({food_id: String(i.food_id), quantity_g: String(i.quantity_g)}))});
    setNotice(""); setError(""); setDeleting(null);
    formRef.current?.scrollIntoView({behavior: "smooth", block: "start"});
  }
  return <>
    <div className="diary-toolbar">
      <div><span className="eyebrow">SEU DIÁRIO ALIMENTAR</span><h2>Um registro de cada momento.</h2></div>
      <label className="date-filter">Consultar dia<input type="date" aria-label="Consultar dia" value={day} disabled={busy} onChange={e => changeDay(e.target.value)} required /></label>
    </div>
    {error && <p className="message error" role="alert">{error}</p>}
    {notice && <p className="message success" role="status">{notice}</p>}
    <div className="meal-grid">
      <section className="card meal-form" ref={formRef}>
        <h2>{editing ? "Editar refeição" : "Registrar refeição"}</h2>
        <p className="muted">Escolha os alimentos e informe a quantidade consumida.</p>
        {foods.length === 0 ? <p className="empty">Primeiro, cadastre um alimento na aba “Alimentos”. Depois volte aqui para montar sua refeição.</p> :
        <form onSubmit={save}>
          <fieldset disabled={busy}>
            <div className="two">
              <label>Data<input type="date" value={form.date} onChange={e => setForm({...form, date: e.target.value})} required /></label>
              <label>Refeição<select value={form.meal_type} onChange={e => setForm({...form, meal_type: e.target.value})}>{Object.entries(types).map(([k,v]) => <option key={k} value={k}>{v}</option>)}</select></label>
            </div>
            <label>Horário da refeição (opcional)<input type="time" step="60" value={form.meal_time} onChange={e => setForm({...form, meal_time: e.target.value})} /></label>
            <div className="item-list">{form.items.map((item, index) => <div className="meal-item-input" key={index}>
              <label>Alimento {index+1}<select value={item.food_id} onChange={e => itemChange(index,"food_id",e.target.value)} required>
                <option value="">Selecione</option>
                {foods.map(f => <option key={f.id} value={f.id} disabled={form.items.some((v,i) => i !== index && Number(v.food_id) === f.id)}>{f.name}</option>)}
              </select></label>
              <label>Quantidade (g)<input type="number" min="0.1" max="10000" step="0.1" value={item.quantity_g} onChange={e => itemChange(index,"quantity_g",e.target.value)} required /></label>
              {form.items.length > 1 && <button type="button" className="remove-item" aria-label={`Remover alimento ${index+1}`} onClick={() => setForm({...form,items:form.items.filter((_,i) => i !== index)})}>×</button>}
            </div>)}</div>
            <button className="secondary" type="button" disabled={form.items.length >= Math.min(foods.length,50)} onClick={() => setForm({...form,items:[...form.items,{food_id:"",quantity_g:"100"}]})}>+ Adicionar outro alimento</button>
            <label>Observações <span className="muted">(opcional)</span><textarea maxLength={500} rows={3} placeholder="Algo que você gostaria de lembrar?" value={form.notes} onChange={e => setForm({...form,notes:e.target.value})} /></label>
            <button type="submit">{busy ? "Salvando…" : editing ? "Salvar alterações" : "Registrar refeição"}</button>
            {editing && <button type="button" className="secondary" onClick={() => reset()}>Cancelar edição</button>}
          </fieldset>
        </form>}
      </section>
      <section className="diary" aria-label="Refeições do dia" aria-busy={loading}>
        <div className="diary-heading"><h2>Refeições do dia</h2><span className="badge">{loading ? "…" : `${meals.length} registro${meals.length === 1 ? "" : "s"}`}</span></div>
        {loading ? <p className="empty">Carregando refeições…</p> : meals.length === 0 ? <div className="card empty"><span className="empty-icon">♧</span><h3>Seu dia começa aqui.</h3><p>Nenhuma refeição registrada nesta data.<br/>Adicione a primeira no formulário ao lado.</p></div> :
          Object.entries(types).map(([type,label]) => {
            const group = meals.filter(m => m.meal_type === type);
            return group.length > 0 && <div key={type} className="meal-group"><h3><span>{icons[type]}</span> {label}</h3>{group.map(meal => <article key={meal.id} className="card meal-entry">
              <p className="meal-time">{meal.meal_time ? `Horário: ${meal.meal_time}` : "Horário não informado"}</p>
              <ul>{meal.items.map(item => <li key={item.id}><strong>{item.food.name}</strong><span>{item.quantity_g.toLocaleString("pt-BR")} g</span></li>)}</ul>
              {meal.notes && <p className="meal-notes">{meal.notes}</p>}
              <div className="actions">
                <button type="button" className="secondary" disabled={busy} onClick={() => edit(meal)}>Editar</button>
                <button type="button" className="danger-text" disabled={busy} onClick={() => setDeleting(meal.id)}>Excluir</button>
              </div>
              {deleting === meal.id && <div className="confirm" role="alert"><p>Excluir esta refeição?</p><button type="button" disabled={busy} onClick={() => remove(meal.id)}>Confirmar exclusão</button> <button type="button" className="secondary" disabled={busy} onClick={() => setDeleting(null)}>Cancelar</button></div>}
            </article>)}</div>;
          })}
      </section>
    </div>
  </>;
}
