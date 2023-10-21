select title from movies where year = 2008;

select birth from people where name = 'Emma Stone';

select title from movies where year >= 2018 order by title asc;

select count(*) from ratings where rating = 10.0;

select title, year from movies where title like "Harry Potter%" order by year;

select avg(rating) from ratings where movie_id in (select id from movies where year = 2012);

select title, rating from movies, ratings where movies.id = ratings.movie_id and movies.year = 2010 order by rating desc, title asc;

select name from people, movies, stars where movies.title = "Toy Story" and movies.id = stars.movie_id and stars.person_id = people.id;

select name from people where id in (select person_id from stars where movie_id in (select id from movies where year = 2004)) order by birth;

select name from people where id in (select person_id from directors where movie_id in (select movie_id from ratings where rating >= 9));

select title  from movies, stars, ratings, people where people.name = "Chadwick Boseman" and people.id = stars.person_id and stars.movie_id = ratings.movie_id and ratings.movie_id = movies.id order by ratings.rating desc limit 5;

select title from movies, stars, people where people.name in  ("Bradley Cooper", "Jennifer Lawrence")  and people.id = stars.person_id and stars.movie_id = movies.id group by title having count(title) > 1;

select name from people where id in (select distinct(person_id) from stars where movie_id in (select movie_id from stars where person_id = (select id from people where name = "Kevin Bacon" and birth = 1958)) and person_id != (select id from people where name = "Kevin Bacon" and birth = 1958));
