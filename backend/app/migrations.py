"""Atualizações aditivas para bancos existentes da AC1/AC2."""
from sqlalchemy import inspect, text
from .database import Base

MEAL_DETAILS_VIEW = """
CREATE VIEW vw_refeicoes_detalhadas AS
SELECT m.id AS refeicao_id,
       m.user_id AS usuario_id,
       m.date AS data,
       m.meal_time AS horario,
       CASE m.meal_type
         WHEN 'breakfast' THEN 'Café da manhã'
         WHEN 'lunch' THEN 'Almoço'
         WHEN 'dinner' THEN 'Jantar'
         WHEN 'snack' THEN 'Lanche'
       END AS refeicao,
       f.name AS alimento,
       i.quantity_g AS quantidade_g,
       m.notes AS observacoes
FROM meals m
JOIN meal_items i ON i.meal_id = m.id
JOIN foods f ON f.id = i.food_id
"""


def initialize_database(engine):
    Base.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        columns = {column['name'] for column in inspect(connection).get_columns('meals')}
        if 'meal_time' not in columns:
            # NULL significa horário desconhecido; nunca inventamos horários antigos.
            connection.execute(text('ALTER TABLE meals ADD COLUMN meal_time VARCHAR(5)'))
        if 'vw_refeicoes_detalhadas' not in inspect(connection).get_view_names():
            connection.execute(text(MEAL_DETAILS_VIEW))
