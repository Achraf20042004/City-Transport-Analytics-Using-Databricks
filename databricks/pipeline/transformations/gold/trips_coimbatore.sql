CREATE OR REPLACE VIEW transportation.gold.fait_coimbatore
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'TN01'
);