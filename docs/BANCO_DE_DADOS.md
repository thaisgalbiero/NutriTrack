# Como o banco do NutriTrack funciona

Uma refeição pode conter vários alimentos. Por isso, o banco divide a informação em tabelas relacionadas:

| Tabela | O que armazena |
|---|---|
| users | Pessoas cadastradas no sistema |
| foods | Nome e informações nutricionais de cada alimento |
| meals | Usuário, data, horário, tipo e observações da refeição |
| meal_items | Ligação entre a refeição e seus alimentos, com quantidade em gramas |

O campo `meal_id` em `meal_items` aponta para `id` em `meals`. O campo `food_id` aponta para `id` em `foods`. Assim, cada item identifica exatamente qual alimento foi usado em qual refeição.

Guardar uma lista de nomes dentro da tabela `meals` dificultaria a consulta e a manutenção. A estrutura atual permite reutilizar o mesmo alimento em várias refeições. Os nomes exibidos correspondem ao catálogo atual.

## Ver os nomes dos alimentos junto com a refeição

No visualizador SQLite, abra o arquivo `backend/nutritrack.db` desta versão e procure a seção **Views / Visualizações**. Selecione **vw_refeicoes_detalhadas**. Atualize ou reabra o banco se a visualização ainda não aparecer.

Ela mostra data, horário, tipo de refeição, nome do alimento e quantidade, com uma linha por alimento. Um almoço com cinco alimentos aparece em cinco linhas com o mesmo `refeicao_id`.

A visualização não duplica os registros: é uma consulta que junta as tabelas e sempre reflete os dados atuais. É destinada à inspeção local do banco; inclui os usuários presentes nele. A aplicação continua filtrando as refeições por usuário autenticado.

Se sua extensão tiver um editor SQL, execute:

```sql
SELECT refeicao_id, data, horario, refeicao, alimento, quantidade_g
FROM vw_refeicoes_detalhadas
ORDER BY data DESC, refeicao_id, alimento;
```

## Horário

O formulário agora oferece **Horário da refeição (opcional)** no cadastro e na edição. O horário aparece também no cartão da refeição e é guardado no campo `meals.meal_time`, no formato de 24 horas `HH:mm`.

É o horário informado da refeição, e não a hora em que o registro foi criado. Não há conversão automática de fuso horário. Refeições anteriores mantêm o valor vazio (`NULL`), exibido como **Horário não informado**; clique em Editar para preenchê-lo. Deixar o campo vazio continua permitido.

## Explicação para a apresentação

“O banco relaciona usuários, refeições, alimentos e itens das refeições. Cada item registra o alimento e sua quantidade. Para facilitar a leitura, criei uma visualização que reúne os nomes dos alimentos, as quantidades, a data e o horário. Essa visualização consulta as tabelas sem duplicar os dados.”
