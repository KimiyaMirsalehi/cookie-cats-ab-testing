-- ============================================================
-- COOKIE CATS — SQL PLAYER ENGAGEMENT ANALYSIS
-- ============================================================

SELECT
    version,

    COUNT(*) AS total_players,

    ROUND(AVG(sum_gamerounds), 2) AS mean_rounds,

    MEDIAN(sum_gamerounds) AS median_rounds,

    ROUND(STDDEV_SAMP(sum_gamerounds), 2) AS std_rounds,

    MIN(sum_gamerounds) AS min_rounds,

    MAX(sum_gamerounds) AS max_rounds,

    QUANTILE_CONT(sum_gamerounds, 0.25) AS p25_rounds,

    QUANTILE_CONT(sum_gamerounds, 0.75) AS p75_rounds,

    QUANTILE_CONT(sum_gamerounds, 0.95) AS p95_rounds,

    QUANTILE_CONT(sum_gamerounds, 0.99) AS p99_rounds,

    COUNT(*) FILTER (
        WHERE sum_gamerounds = 0
    ) AS zero_round_players,

    ROUND(
        COUNT(*) FILTER (
            WHERE sum_gamerounds = 0
        ) * 100.0 / COUNT(*),
        2
    ) AS zero_round_percentage

FROM players

GROUP BY version

ORDER BY version;