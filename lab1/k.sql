DROP VIEW IF EXISTS studentview;
CREATE VIEW studentview AS
SELECT ssn, first_name, last_name, course_code, grade, course_name, credits
FROM students
JOIN taken_courses
USING (ssn)
JOIN courses
USING (course_code);
SELECT sum(credits)
FROM studentview 
WHERE ssn = '910101-1234'
