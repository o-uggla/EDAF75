SELECT students.ssn, first_name, last_name, coalesce(totcredits, 0)
FROM students
LEFT JOIN (
  SELECT ssn, sum(credits) as totcredits
  FROM taken_courses
  LEFT JOIN (
    SELECT course_code, credits
    FROM courses
  ) AS coursecredits
  ON taken_courses.course_code = coursecredits.course_code
  GROUP BY ssn
) AS studentcredits
ON students.ssn = studentcredits.ssn
