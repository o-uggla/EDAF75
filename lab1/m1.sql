SELECT first_name, last_name, course_code
FROM students
LEFT OUTER JOIN taken_courses
ON students.ssn = taken_courses.ssn
WHERE course_code IS NULL 
