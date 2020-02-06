SELECT first_name, last_name, ssn
FROM students 
WHERE ssn LIKE '85%'
ORDER BY last_name, first_name
