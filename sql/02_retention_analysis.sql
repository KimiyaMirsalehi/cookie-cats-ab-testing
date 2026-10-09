-- ============================================================
-- COOKIE CATS — PLAYER RETENTION ANALYSIS
-- ============================================================

WITH retention_summary AS (

    SELECT
        version,

        COUNT(*) AS total_players,

        SUM(
            CASE
                WHEN retention_1 = TRUE THEN 1
                ELSE 0
            END
        ) AS day1_retained,

        SUM(
            CASE
                WHEN retention_7 = TRUE THEN 1
                ELSE 0
            END
        ) AS day7_retained

    FROM players

    GROUP BY version

)

SELECT
    version,

    total_players,

    day1_retained,

    day7_retained,

    ROUND(
        day1_retained * 100.0 / total_players,
        3
    ) AS day1_retention_pct,

    ROUND(
        day7_retained * 100.0 / total_players,
        3
    ) AS day7_retention_pct

FROM retention_summary

ORDER BY version;