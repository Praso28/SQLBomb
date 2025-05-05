CREATE TABLE bombs (
  bomb_id INTEGER PRIMARY KEY AUTOINCREMENT,
  location TEXT,
  voltage_readings TEXT, -- SQLite doesn't have array type, so we'll store as text
  last_maintained TEXT,  -- SQLite doesn't have timestamp, using TEXT
  signal_strength INTEGER,
  battery_level INTEGER,
  frequency_pattern TEXT,
  device_signature TEXT
);

CREATE TABLE suspects (
  suspect_id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  access_level INTEGER,
  last_login TEXT  -- SQLite doesn't have timestamp, using TEXT
);

CREATE TABLE bomb_components (
  component_id INTEGER PRIMARY KEY AUTOINCREMENT,
  bomb_id INTEGER,
  component_name TEXT,
  material TEXT,
  activation_code TEXT,
  FOREIGN KEY (bomb_id) REFERENCES bombs(bomb_id)
);

CREATE TABLE access_logs (
  log_id INTEGER PRIMARY KEY AUTOINCREMENT,
  suspect_id INTEGER,
  bomb_id INTEGER,
  access_time TEXT,  -- SQLite doesn't have timestamp, using TEXT
  action_performed TEXT,
  FOREIGN KEY (suspect_id) REFERENCES suspects(suspect_id),
  FOREIGN KEY (bomb_id) REFERENCES bombs(bomb_id)
);
