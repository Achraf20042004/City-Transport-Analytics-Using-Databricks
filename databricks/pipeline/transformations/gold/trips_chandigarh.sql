CREATE OR REPLACE VIEW transportation.gold.fait_Chandigarh
AS (
SELECT *
FROM transportation.gold.fait_voyage
WHERE city_id = 'CH01'
);




