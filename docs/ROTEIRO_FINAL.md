# NutriTrack — roteiro de gravação (5–7 minutos)

## Preparação
Abra ABRIR_NUTRITRACK.command na pasta do projeto. Aguarde API e interface iniciarem.
Tenha abertas as páginas do sistema, http://127.0.0.1:8000/docs, GitHub e board.
Use uma conta de demonstração e confira os valores por 100 g dos alimentos.
No Mac, pressione Shift + Command + 5, escolha a área da tela e selecione o microfone em Opções. Faça um teste curto de áudio antes da gravação completa.

## 0:00 — Apresentação
“Sou Thaís Sgalbiero Ramalho e este é o NutriTrack, meu sistema de registro alimentar. Nesta etapa acrescentei análise de calorias e macronutrientes e acompanhamento de metas ao diário de refeições.”

## 0:30 — Acesso e catálogo
Mostre cadastro/login. Na aba Alimentos, cadastre “Alimento de demonstração” com valores fictícios por 100 g: 200 kcal, 10 g proteínas, 20 g carboidratos e 5 g gorduras.
Explique que os números são exemplos para demonstrar o cálculo.

## 1:20 — Diário
Registre almoço na data de hoje, horário 12:30, com 150 g do alimento.
Mostre a refeição e explique as opções de edição, exclusão e consulta por data.

## 2:10 — Resumo e metas
Abra Resumo e metas na mesma data. Resultado esperado: 300 kcal, 15 g proteínas, 30 g carboidratos e 7,5 g gorduras.
“O sistema multiplica o valor por 100 g pela quantidade consumida e divide por 100.”
Salve metas fictícias: 600 kcal, 30 g proteínas, 60 g carboidratos e 15 g gorduras. Os quatro indicadores devem mostrar 50%.
“As metas são definidas pelo usuário e persistem no banco.”

## 3:10 — Edição e persistência
Edite a refeição para 100 g, volte ao resumo e mostre 200 kcal, 10 g proteínas, 20 g carboidratos e 5 g gorduras.
Atualize a página para demonstrar persistência. Consulte uma data sem refeições.
Se desejar demonstrar exclusão, crie um segundo registro de teste e exclua apenas esse registro.

## 4:10 — Código e API
Mostre frontend/src/Summary.jsx (interface), backend/app/main.py (rota /dashboard e cálculo), models.py (Goal, Meal, MealItem) e backend/tests/test_ac3.py (testes).
Explique: React/Vite → API FastAPI → SQLAlchemy → SQLite.
Abra /docs para mostrar as rotas de refeições, metas e dashboard. Não exponha senhas ou tokens na gravação.

## 5:10 — GitHub e board
Abra https://github.com/thaisgalbiero/NutriTrack e mostre o código e documentação da AC3.
Abra https://github.com/users/thaisgalbiero/projects/3/views/1 e mostre as tarefas e seus estados reais.
Encerre explicando as funcionalidades entregues.

## Checklist de entrega
- Conferir vídeo com imagem e áudio, sem cortes nas demonstrações principais.
- Publicar vídeo e testar o acesso ao link.
- Conferir acesso do professor ao GitHub e ao board.
- Colar os três links no Classroom e concluir a entrega individualmente.
- Usar o novo vídeo da entrega final, não reutilizar automaticamente o link da AC1.
