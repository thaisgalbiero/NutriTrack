-- Estrutura conceitual do banco NutriTrack AC1
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL
);

CREATE TABLE foods (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    calories FLOAT NOT NULL,
    protein FLOAT NOT NULL,
    carbs FLOAT NOT NULL,
    fat FLOAT NOT NULL
);

-- AC2: criação aditiva; não remove usuários ou alimentos da AC1.
CREATE TABLE meals (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    date DATE NOT NULL,
    meal_type VARCHAR(20) NOT NULL CHECK (meal_type IN ('breakfast','lunch','dinner','snack')),
    notes VARCHAR(500) NOT NULL DEFAULT ''
);
CREATE INDEX ix_meals_user_id ON meals(user_id);
CREATE INDEX ix_meals_date ON meals(date);
CREATE TABLE meal_items (
    id INTEGER PRIMARY KEY,
    meal_id INTEGER NOT NULL REFERENCES meals(id),
    food_id INTEGER NOT NULL REFERENCES foods(id),
    quantity_g FLOAT NOT NULL CHECK (quantity_g > 0 AND quantity_g <= 10000)
);
CREATE INDEX ix_meal_items_meal_id ON meal_items(meal_id);
-- Ao excluir uma refeição pela API, o ORM remove seus itens na mesma transação.
