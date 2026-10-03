# AC2 — Registro de refeições

Projeto: NutriTrack
Aluna: Thaís Sgalbiero Ramalho
Matrícula: 2402934

## Objetivo do sprint
Evoluir a AC1 com um diário alimentar integrado ao React, à API FastAPI e ao banco SQLite. O usuário autenticado registra refeições com alimentos do catálogo, quantidades em gramas, data e observações.

## Funcionalidades implementadas
- Café da manhã, almoço, jantar e lanche.
- Uma ou várias refeições de cada tipo no mesmo dia.
- Vários alimentos por refeição, com quantidade individual.
- Consulta das refeições por data, edição e exclusão com confirmação.
- Registros vinculados à conta autenticada.
- Validações: refeição não pode ficar vazia, quantidades devem ser positivas, alimentos precisam existir e não podem se repetir na mesma refeição.
- Feedback de sucesso, carregamento, erros e estado vazio.
- Cadastro e listagem de alimentos da AC1 preservados na aba Alimentos.

O catálogo de alimentos continua compartilhado, conforme a AC1. As refeições são privadas por usuário. Cálculo de calorias, metas e gráficos permanecem para a AC3, seguindo o planejamento anterior.

## Banco e API
Tabelas novas: `meals` (usuário, data, tipo, observações) e `meal_items` (refeição, alimento, quantidade em gramas). São criadas automaticamente ao iniciar a API, sem apagar as tabelas da AC1. O script em `database/schema.sql` documenta a estrutura e não precisa ser executado manualmente sobre o banco existente.

| Método | Rota | Função |
|---|---|---|
| POST | /meals | Registrar uma refeição |
| GET | /meals?date=2026-10-02 | Consultar um dia |
| PUT | /meals/{id} | Editar uma refeição própria |
| DELETE | /meals/{id} | Excluir uma refeição própria |

Todas as rotas exigem autenticação JWT. A tentativa de editar ou excluir refeição de outra conta retorna 404.

## Roteiro de apresentação — aproximadamente 4 minutos
1. **Apresentação:** “Olá, sou Thaís Sgalbiero Ramalho. Na AC1 do NutriTrack implementei cadastro, login e catálogo de alimentos. Nesta segunda etapa, desenvolvi o registro de refeições.”
2. **Entrar no sistema:** mostrar as abas Minhas refeições e Alimentos. Explicar que os alimentos cadastrados na primeira etapa são reutilizados.
3. **Registrar:** escolher uma data, selecionar Almoço, adicionar um alimento e informar 150 gramas. Se houver outro alimento no catálogo, adicioná-lo à mesma refeição. Salvar.
4. **Consultar:** mostrar a refeição na lista e atualizar a página para demonstrar persistência.
5. **Editar:** alterar a quantidade de 150 para 180 gramas e mostrar o resultado.
6. **Data:** consultar outro dia sem registros e voltar à data usada.
7. **Excluir:** usar uma refeição de teste, clicar em Excluir e confirmar.
8. **Banco:** abrir a cópia do arquivo `backend/nutritrack.db` desta versão e mostrar `meals` e `meal_items`. Explicar a ligação entre usuário, refeição e alimento. Não usar o banco da pasta antiga para demonstrar registros feitos nesta versão.
9. **Arquitetura:** “A interface React envia os dados à API FastAPI. A API valida os campos e identifica o usuário pelo token. O SQLAlchemy salva a refeição e seus itens no SQLite.”
10. **Encerramento:** mostrar o código e o Board depois de atualizar ambos. “A próxima etapa será o cálculo de calorias e macronutrientes e a análise nutricional.”

## Board e entrega
O código da AC2 está disponível neste repositório. O card “Registro de refeições” corresponde à funcionalidade entregue neste sprint.

Descrição da entrega do card “Registro de refeições”:

> Implementado cadastro, consulta por data, edição e exclusão de refeições. Cada refeição contém tipo, data, alimentos, quantidades em gramas e observações. Os registros pertencem ao usuário autenticado e são persistidos no banco de dados.

- Repositório: https://github.com/thaisgalbiero/NutriTrack
- Board: https://github.com/users/thaisgalbiero/projects/3/views/1
- Vídeo da AC2: gravar e inserir o novo link. O vídeo da AC1 não demonstra esta etapa.

## Verificações executadas
- Build de produção do frontend.
- Integração HTTP: cadastro/login, alimentos, CRUD de refeições, quatro tipos, filtro por data, validação de dados, isolamento entre contas e persistência após reiniciar a API.
- Verificação no navegador: login, criação de refeição e edição da quantidade, com resultado visível.

Para repetir o teste automatizado, execute no diretório backend:

```sh
python -m unittest discover -s tests -v
```

O teste utiliza banco temporário próprio e não altera seus dados.

## Horário e visualização do banco
O cadastro e a edição permitem informar o horário (HH:mm). Refeições anteriores ficam sem horário até serem editadas. A view `vw_refeicoes_detalhadas` exibe os nomes dos alimentos e suas quantidades ao lado da refeição. Consulte [Como o banco funciona](BANCO_DE_DADOS.md).
