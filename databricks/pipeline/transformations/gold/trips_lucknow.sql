CREATE OR REPLACE VIEW transportation.gold.fait_lucknow
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'UP01'
);