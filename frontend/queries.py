sqlite_metrics={
    "latestCovid":"""  SELECT combinedKey, confirmed, deaths
                        FROM daily
                        WHERE lastUpdate=(SELECT max(lastUpdate) from daily)
                        Order by confirmed desc"""
}