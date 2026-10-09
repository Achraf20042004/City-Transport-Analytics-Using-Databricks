CREATE OR REPLACE VIEW transportation.gold.fait_visakhapatnam
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'AP01'
);