/*
Use this query to check the size of a database, to give you an idea of how
big you need to configure its PVC in Postgres
*/
SELECT
  datname                                AS database,
  pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;
