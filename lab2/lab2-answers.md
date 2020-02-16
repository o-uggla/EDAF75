
theaters (_t_name_, t_capacity);
movies (_m_title_,_m_year_,m_imdb_key,m_duration);
performances (_perf_date_, _perf_time_, /_t_name_/, /m_title/ ,/m_year/, );
customers (_username_, fullname, password);
tickets (_ticket_id_, /username/, /t_name/, /perf_date/, /perf_time/);
                               
7. There are at least two ways of keeping track of the number of seats available for each performance – describe them both, with their upsides and downsides (write your answer in lab2-answers.md).

For your own database, you can choose either method, but you should definitely be aware of both.

We have a number for the total available seats, and then for a performance we first set the available seats to the theaters capacity, then when a ticket is sold we decrement the availabel ticket colun for a performance.

We can also keep track with taking the capacity - the count() for the number of tickets sold for that performance. One takes more plale in the database. The other method requires more calculations oververhead.