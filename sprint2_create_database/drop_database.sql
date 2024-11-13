-- Drop tables with foreign key dependencies first
DROP TABLE IF EXISTS Book_Awards CASCADE;
DROP TABLE IF EXISTS Book_Series CASCADE;
DROP TABLE IF EXISTS Book_Genre CASCADE;
DROP TABLE IF EXISTS Book_Publisher CASCADE;
DROP TABLE IF EXISTS Book_Author CASCADE;

-- Drop standalone tables or tables with only dependencies on previously dropped tables
DROP TABLE IF EXISTS Awards CASCADE;
DROP TABLE IF EXISTS Series CASCADE;
DROP TABLE IF EXISTS Genre CASCADE;
DROP TABLE IF EXISTS Publisher CASCADE;
DROP TABLE IF EXISTS Author CASCADE;
DROP TABLE IF EXISTS Book CASCADE;

-- Drop sequences
DROP SEQUENCE IF EXISTS smallint_sequence CASCADE;

-- Drop custom types
DROP TYPE IF EXISTS Gender CASCADE;
DROP TYPE IF EXISTS Status CASCADE;