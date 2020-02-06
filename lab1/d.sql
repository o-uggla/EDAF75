SELECT first_name, last_name, ssn
FROM students 
WHERE substr(ssn, 10, 1) % 2 = 0
ORDER BY last_name, first_name
