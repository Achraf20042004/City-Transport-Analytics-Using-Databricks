CREATE OR REPLACE VIEW transportation.gold.fait_jaipur
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'RJ01'
);