SELECT first_name, last_name
FROM students
WHERE ssn NOT IN (
  SELECT ssn
  FROM taken_courses
  GROUP BY ssn
)
