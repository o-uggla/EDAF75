WITH multiplenames (first_name, last_name, name) as 
  (
  SELECT first_name, last_name, (first_name || last_name) as name
  FROM students
  GROUP BY name
  HAVING count() > 1
  )
SELECT ssn, first_name, last_name 
FROM students as s
WHERE (s.first_name || s.last_name) in (SELECT name FROM multiplenames)

