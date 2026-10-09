CREATE OR REPLACE VIEW transportation.gold.fait_indore
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'MP01'
);