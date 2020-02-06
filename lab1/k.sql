SELECT sum(credits)
FROM courses
WHERE course_code in 
(SELECT course_code
FROM taken_courses 
WHERE ssn = '910101-1234')
