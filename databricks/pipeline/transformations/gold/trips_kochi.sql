CREATE OR REPLACE VIEW transportation.gold.fait_kochi
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'KL01'
);