SELECT
    version,
    COUNT(*) AS total_players,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage_of_players
FROM players
GROUP BY version
ORDER BY version;