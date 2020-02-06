SELECT course_code, course_name
FROM courses
WHERE course_code IN (
SELECT course_code 
FROM taken_courses
GROUP BY course_code
ORDER BY avg(grade) ASC
LIMIT 5
)
