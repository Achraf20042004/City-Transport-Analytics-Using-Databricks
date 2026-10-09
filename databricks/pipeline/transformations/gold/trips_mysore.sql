CREATE OR REPLACE VIEW transportation.gold.fait_Mysore
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'KA01'
);