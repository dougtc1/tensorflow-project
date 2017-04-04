SELECT  p1.yearID as year1, p2.yearID as year2, p1.playerID, p1.W, p1.L, p1.G, p1.IPouts, p1.H,
	    p1.ER, p1.SO/(p1.IPouts/27), p1.BB/(p1.IPouts/27), p1.BAOpp, tablita.AVG, p1.ERA, p2.ERA as era_2

FROM Pitching as p1, 
	 Pitching as p2, 
	 (
	  SELECT yearID as year, lgid as liga, AVG(H/AB) as AVG 
	  FROM Batting 
	  WHERE H != 0
	  		AND AB > 40
	  GROUP BY year, lgID
	 ) as tablita

WHERE p1.playerID = p2.playerID 
	  AND p1.yearID > 1949
	  AND p1.yearID + 1 = p2.yearID
	  AND p1.IPouts > 60
	  AND p2.IPouts > 60
	  AND tablita.year = p1.yearID
	  AND tablita.liga = p1.lgID
	  AND p1.ERA != ''
	  AND p1.W != ''
	  AND p1.L != ''
	  AND p1.G != ''
	  AND p1.G != 0
	  AND p1.IPouts != ''
	  AND p1.ER != ''
	  AND p1.SO != ''
	  AND p1.BB != ''
	  AND p1.BAOpp != ''
	  AND p1.BAOpp != 0
	  AND p2.ERA != ''

ORDER BY p1.yearID, p1.playerID
INTO OUTFILE '/var/lib/mysql-files/dataset-2.txt'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
