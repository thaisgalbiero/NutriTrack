import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://127.0.0.1:8000";

async function api(path, options = {}) {
  const token = localStorage.getItem("token");
  const headers = {"Content-Type": "application/json", ...(options.headers || {})};
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(`${API}${path}`, {...options, headers});
  const data = await response.json();
  if (!response.ok) throw new Error(data.detail || "Erro na requisição");
  return data;
}

function Auth({ onLogin }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({name:"", email:"", password:""});

  async function submit(e) {
    e.preventDefault();
    try {
      if (mode === "register") {
        await api("/auth/register", {method:"POST", body:JSON.stringify(form)});
        alert("Cadastro realizado! Agora faça login.");
        setMode("login");
      } else {
        const data = await api("/auth/login", {method:"POST", body:JSON.stringify({
          email: form.email, password: form.password
        })});
        localStorage.setItem("token", data.access_token);
        onLogin();
      }
    } catch (err) {
      alert(err.message);
    }
  }

  return <div className="auth">
    <div className="card">
      <div className="brand">🥗 NutriTrack</div>
      <h1>{mode === "login" ? "Bem-vinda!" : "Criar conta"}</h1>
      <p className="muted">{mode === "login" ? "Entre para acompanhar sua alimentação." : "Comece a registrar seus hábitos."}</p>
      <form onSubmit={submit}>
        {mode === "register" && <input placeholder="Nome" value={form.name} onChange={e=>setForm({...form,name:e.target.value})} required />}
        <input type="email" placeholder="E-mail" value={form.email} onChange={e=>setForm({...form,email:e.target.value})} required />
        <input type="password" placeholder="Senha (mín. 6 caracteres)" value={form.password} onChange={e=>setForm({...form,password:e.target.value})} required />
        <button>{mode === "login" ? "Entrar" : "Cadastrar"}</button>
      </form>
      <button className="link" onClick={()=>setMode(mode==="login"?"register":"login")}>
        {mode === "login" ? "Ainda não tenho conta" : "Já tenho uma conta"}
      </button>
    </div>
  </div>
}

function Dashboard({onLogout}) {
  const [foods, setFoods] = useState([]);
  const [food, setFood] = useState({name:"", calories:"", protein:"", carbs:"", fat:""});

  async function loadFoods() {
    try { setFoods(await api("/foods")); }
    catch(err) { if (err.message.includes("Token")) onLogout(); }
  }

  React.useEffect(()=>{ loadFoods(); }, []);

  async function addFood(e) {
    e.preventDefault();
    try {
      await api("/foods", {method:"POST", body:JSON.stringify({
        name: food.name,
        calories: Number(food.calories),
        protein: Number(food.protein),
        carbs: Number(food.carbs),
        fat: Number(food.fat)
      })});
      setFood({name:"", calories:"", protein:"", carbs:"", fat:""});
      loadFoods();
    } catch(err) { alert(err.message); }
  }

  return <div className="app">
    <header>
      <div className="brand">🥗 NutriTrack</div>
      <button className="logout" onClick={()=>{localStorage.removeItem("token");onLogout()}}>Sair</button>
    </header>
    <main>
      <section className="hero">
        <div>
          <span className="eyebrow">AC1 • SPRINT 1</span>
          <h1>Seu primeiro passo para entender seus hábitos.</h1>
          <p>Cadastre alimentos e construa sua base nutricional.</p>
        </div>
      </section>
      <section className="grid">
        <div className="card">
          <h2>Cadastrar alimento</h2>
          <form onSubmit={addFood}>
            <input placeholder="Nome do alimento" value={food.name} onChange={e=>setFood({...food,name:e.target.value})} required />
            <div className="two">
              <input type="number" step="0.1" placeholder="Calorias" value={food.calories} onChange={e=>setFood({...food,calories:e.target.value})} required />
              <input type="number" step="0.1" placeholder="Proteínas (g)" value={food.protein} onChange={e=>setFood({...food,protein:e.target.value})} required />
              <input type="number" step="0.1" placeholder="Carboidratos (g)" value={food.carbs} onChange={e=>setFood({...food,carbs:e.target.value})} required />
              <input type="number" step="0.1" placeholder="Gorduras (g)" value={food.fat} onChange={e=>setFood({...food,fat:e.target.value})} required />
            </div>
            <button>Adicionar alimento</button>
          </form>
        </div>
        <div className="card">
          <h2>Alimentos cadastrados</h2>
          {foods.length === 0 ? <p className="muted">Nenhum alimento cadastrado.</p> :
          <div className="food-list">{foods.map(f=>
            <div className="food" key={f.id}>
              <strong>{f.name}</strong>
              <span>{f.calories} kcal • P {f.protein}g • C {f.carbs}g • G {f.fat}g</span>
            </div>
          )}</div>}
        </div>
      </section>
    </main>
  </div>
}

function App() {
  const [logged, setLogged] = useState(!!localStorage.getItem("token"));
  return logged ? <Dashboard onLogout={()=>setLogged(false)} /> : <Auth onLogin={()=>setLogged(true)} />;
}

createRoot(document.getElementById("root")).render(<App />);
