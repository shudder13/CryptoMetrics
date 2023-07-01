DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS price_history;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE price_history (
  symbol TEXT NOT NULL,
  date DATE NOT NULL,
  price REAL NOT NULL,
  PRIMARY KEY (symbol, date)
);
