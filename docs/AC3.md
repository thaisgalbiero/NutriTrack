# AC3 — Análise nutricional e metas

A AC3 amplia o diário de refeições existente da AC2. Não cria um segundo diário.

## Funcionalidades
- Aba Resumo e metas, com consulta por data e quantidade de refeições.
- Totais diários de calorias, proteínas, carboidratos e gorduras.
- Metas individuais persistidas em SQLite e percentual atingido, inclusive acima de 100%.
- Totais recalculados ao abrir o resumo após cadastrar, editar ou excluir refeições.
- Dados de refeições e metas restritos ao usuário autenticado; catálogo de alimentos compartilhado.

## Regra de cálculo
Os valores dos alimentos são por 100 g. Cada contribuição é valor × quantidade_g / 100.
As calorias são as informadas no catálogo; não são estimadas a partir dos macronutrientes.
Confira a unidade dos alimentos cadastrados antes da AC3. Os dados antigos não são convertidos automaticamente.
As metas são informadas pelo usuário, sem valores predefinidos. A meta atual se aplica à comparação de qualquer data; não há histórico de mudanças de meta.

## API e banco
- GET /dashboard?date=AAAA-MM-DD: totais, número de refeições, metas e percentuais.
- GET /goals: metas atuais ou null.
- PUT /goals: salva as quatro metas, todas positivas e finitas.
- Tabela goals: uma linha por usuário. Criação aditiva na inicialização; refeições existentes preservadas.

## Verificação
No backend: `.venv/bin/python -m unittest discover -s tests -v`.
Na raiz: `npm run build --prefix frontend`.
A suíte cobre AC1/AC2, migração, cálculos proporcionais, datas, isolamento entre usuários, limites, persistência após reinício e recálculo após edição/exclusão.

## Entrega informada pela aluna
Vídeo demonstrando a funcionalidade, link do board e link do código-fonte, entregues individualmente no Classroom.
Não foi fornecida rubrica adicional. Ver roteiro em ROTEIRO_FINAL.md.
