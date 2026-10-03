import unittest
from sqlalchemy import create_engine, text, inspect
from app import models
from app.migrations import initialize_database

class MigrationTest(unittest.TestCase):
    def test_old_database_preserves_meal_and_named_food(self):
        engine = create_engine('sqlite://')
        with engine.begin() as db:
            db.execute(text('CREATE TABLE meals (id INTEGER PRIMARY KEY, user_id INTEGER, date DATE, meal_type VARCHAR(20), notes VARCHAR(500))'))
            db.execute(text("INSERT INTO meals VALUES (1, 1, '2026-10-02', 'lunch', 'Existente')"))
        initialize_database(engine)
        initialize_database(engine)
        with engine.begin() as db:
            db.execute(text("INSERT INTO foods VALUES (1, 'Arroz branco', 130, 2.7, 28.2, 0.3)"))
            db.execute(text('INSERT INTO meal_items VALUES (1, 1, 1, 150)'))
            self.assertEqual(db.execute(text('SELECT horario, refeicao, alimento, quantidade_g, observacoes FROM vw_refeicoes_detalhadas')).one(), (None, 'Almoço', 'Arroz branco', 150, 'Existente'))
            self.assertEqual(len(inspect(db).get_columns('meals')), 6)
        engine.dispose()
