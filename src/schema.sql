CREATE TABLE reference (
  id SERIAL PRIMARY KEY,
  ref_type TEXT NOT NULL,
  citation_key TEXT NOT NULL,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  year INT NOT NULL,
  booktitle TEXT,
  publisher TEXT,
  journal TEXT,
  pages TEXT,
  volume TEXT,
  edition TEXT,
  doi TEXT,
  chapter TEXT,
  address TEXT
)