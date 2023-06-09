/*What is the most common room type in NYC Airbnb listings?*/

SELECT room_type,count(*)
FROM room_types
GROUP BY room_type

/*What is the average price of a listing by room type*/

SELECT ROUND(avg(price),2),room_type
FROM prices as p
JOIN room_types as rt
ON p.listing_id = rt.listing_id
GROUP BY room_type

/*Which borough has the highest average price per month?*/

SELECT TRUNC(avg(price_per_month)::numeric,2), borough
FROM prices
GROUP BY borough;

/*How many listings of each room type are in each borough?*/

SELECT p.borough, rt.room_type,TRUNC(count(p.listing_id)::numeric, 0) as listing_count
FROM prices as p
JOIN room_types as rt
ON p.listing_id = rt.listing_id
GROUP BY p.borough, rt.room_type;

/*How many listings in each room type category have a price of over $500 per night?*/

SELECT rt.room_type, COUNT(DISTINCT p.listing_id) as listing_count
FROM prices as p
JOIN room_types as rt
ON p.listing_id = rt.listing_id
WHERE p.price > 500
GROUP BY rt.room_type;

/*What is the distribution of listing prices by borough?*/

SELECT p.borough,
       MIN(p.price) as min_price,
       MAX(p.price) as max_price,
       ROUND(AVG(p.price),2) as avg_price
FROM prices as p
GROUP BY p.borough

/*What is the estimated amount of revenue generated by hosts in each borough?*/

SELECT p.borough, SUM(p.price * r.booked_days_365) as total_revenue
FROM prices as p

JOIN reviews as r ON p.listing_id = r.listing_id
GROUP BY p.borough;

/*What is the average price per month for listings in each neighborhood?*/

SELECT p.neighbourhood, rt.room_type, AVG(p.price_per_month) AS average_price_per_month
FROM prices AS p
JOIN room_types AS rt
ON p.listing_id = rt.listing_id
GROUP BY 1,2
ORDER BY 3 DESC;

/*How many listings have no reviews?*/

SELECT COUNT(*) AS no_reviews_count
FROM reviews
WHERE listing_id NOT IN (SELECT listing_id FROM reviews);

/*How do the estimated book days correlate with the price of an Airbnb listing in New York City?*/

SELECT CORR(r.booked_days_365, p.price) AS correlation
FROM prices AS p
JOIN reviews AS r ON p.listing_id = r.listing_id;

/*What is the average price per room type for listings that have at least 100 reviews and are available more than 200 days a year?*/

SELECT rt.room_type, ROUND(AVG(p.price),2) AS average_price
FROM room_types AS rt
JOIN prices AS p ON rt.listing_id = p.listing_id
JOIN reviews AS r ON rt.listing_id = r.listing_id
WHERE r.number_of_reviews >= 100 AND r.availability_365 > 200
GROUP BY rt.room_type;

/*How many hosts have more than one listing, and what's the maximum number of listings by a single host name?*/

SELECT COUNT(DISTINCT host_name) AS hosts_with_multiple_listings,
       MAX(listing_count) AS max_listings_by_single_host
FROM (
    SELECT host_name, COUNT(*) AS listing_count
    FROM reviews
    GROUP BY host_name
    HAVING COUNT(*) > 1
) AS subquery;

/*Determine the top 5 hosts who have the highest price_per_month for their listings, considering only hosts who have at least 10 listings.*/

SELECT r.host_name, CAST(avg(p.price_per_month) AS NUMERIC (10,2)) AS average_price_per_month
FROM reviews AS r
INNER JOIN prices AS p
   USING (listing_id)
GROUP BY r.host_name
HAVING COUNT(r.listing_id) >= 10
ORDER BY average_price_per_month DESC
LIMIT 5;

--OR--

SELECT r.host_name, CAST(AVG(p.price_per_month) AS numeric(10,2)) AS average_price_per_month
FROM prices p
JOIN reviews r ON p.listing_id = r.listing_id
WHERE r.host_name IN (
    SELECT host_name
    FROM reviews
    GROUP BY host_name
    HAVING COUNT(*) >= 10
)
GROUP BY r.host_name
ORDER BY average_price_per_month DESC
LIMIT 5;

/*Find the neighborhood(s) that have the highest variance in listing prices.*/

SELECT p.neighbourhood,ROUND(VARIANCE(price),1) AS price_variance
FROM prices p
GROUP BY p.neighbourhood
HAVING VARIANCE(price) = (
    SELECT MAX(price_variance) as max_price_variance
    FROM (
        SELECT neighbourhood, VARIANCE(price) AS price_variance
        FROM prices
        GROUP BY neighbourhood
    ) s
)

-- OR ---

SELECT neighbourhood, ROUND(VARIANCE(price), 1) AS price_variance
FROM prices
WHERE neighbourhood IS NOT NULL
GROUP BY neighbourhood
HAVING VARIANCE(price) = (
    SELECT MAX(Variance)
    FROM (
        SELECT VARIANCE(price) AS Variance
        FROM prices
        WHERE neighbourhood IS NOT NULL
        GROUP BY neighbourhood
    ) AS subquery
);


/* Calculate the average price_per_month for each neighborhood, taking into account only listings
 where the host has a minimum_nights value that is higher than the average minimum_nights value across all listings.*/

 SELECT p.neighbourhood, CAST(AVG(p.price_per_month) AS NUMERIC(10, 2)) AS average_price_per_month
FROM prices p
WHERE p.listing_id IN (
    SELECT r.listing_id
    FROM reviews r
    WHERE r.minimum_nights > (
        SELECT AVG(minimum_nights)
        FROM reviews
    )
)
GROUP BY p.neighbourhood;
