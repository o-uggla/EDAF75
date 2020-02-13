DROP VIEW IF EXISTS studentview;
CREATE VIEW studentview AS
SELECT ssn, first_name, last_name, course_code, grade
FROM students
JOIN taken_courses
USING (ssn);
SELECT course_code
FROM studentview 
WHERE ssn = '910101-1234'
