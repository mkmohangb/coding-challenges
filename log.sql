-- Keep a log of any SQL queries you execute as you solve the mystery.

select description from crime_scene_reports where month=7 and day=28 and street="Humphrey Street";
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
select * from interviews where day=28 and month=7 and transcript like '%bakery%';
-- Ruth - Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene - I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond - As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
-- Cars leaving the bakery parking lot within 10 mins of theft
select license_plate from bakery_security_logs where day=28 and  month = 7 and year=2021 and hour=10 and minute > 15 and minute < 25 and activity='exit';
-- 5P2BI95,94KL13X,6P58WS2,4328GD8,G412CB7,L93JTIZ,322W7JE,0NTHK55,

select account_number from atm_transactions where day=28 and month=7 and year = 2021 and transaction_type = 'withdraw' and atm_location='Leggett Street';
-- 26013199,28500762,28296815,76054385,49610011,16153065,25506511,81061156,

-- earliest flight out of Fiftyville
select id from airports where city='Fiftyville';
select * from flights where origin_airport_id=8 and year = 2021 and month = 7 and day = 29 order by hour, minute limit 1;
-- to NY city
select * from airports where id = 4;

-- phone calls for less than a minute
select * from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60;

-- Thief
select name from people where phone_number in (select caller from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60) and license_plate in (selec
t license_plate from bakery_security_logs where day=28 and  month = 7 and year=2021 and hour=10 and minute > 15 and minute < 25 and activity='exit') and id in (select person_id
from bank_accounts where account_number in  (select account_number from atm_transactions where day=28 and month=7 and year = 2021 and transaction_type = 'withdraw' and atm_locat
ion='Leggett Street')) and passport_number in (select passport_number from passengers where flight_id = (select id from flights where origin_airport_id=8 and year = 2021 and mon
th = 7 and day = 29 order by hour, minute limit 1));

-- city the thief escaped to
select city from airports where id = (select destination_airport_id from flights where origin_airport_id=8 and year = 2021 and month = 7 and day = 29 order by hour, minute limit 1);

-- thief's accomplice
select name from people where phone_number = (select receiver from phone_calls where year = 2021 and month = 7 and day = 28 and duration < 60 and caller = '(367) 555-5533');