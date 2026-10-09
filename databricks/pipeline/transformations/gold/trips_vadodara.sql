CREATE OR REPLACE VIEW transportation.gold.fait_vadodara
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'GJ02'
);