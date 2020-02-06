SELECT first_name, last_name, avggrade
FROM students
LEFT JOIN (
  SELECT ssn, avg(grade) as avggrade
  FROM taken_courses
  GROUP BY ssn
) AS studentavg
ON students.ssn = studentavg.ssn
ORDER BY avggrade DESC
LIMIT 10
