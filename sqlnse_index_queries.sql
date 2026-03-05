/* =====================================================
   MySQL Database: NSE Index Analytics
   ===================================================== */

-- 1️⃣ Create Database
CREATE DATABASE IF NOT EXISTS nse_index_analytics;
USE nse_index_analytics;

-- 2️⃣ Drop table if exists
DROP TABLE IF EXISTS nse_indices;

-- 3️⃣ Create Table (MySQL syntax)
CREATE TABLE nse_indices (
    index_id INT AUTO_INCREMENT PRIMARY KEY,
    index_name VARCHAR(60) NOT NULL,
    market_cap_category VARCHAR(40),
    cagr_1y DECIMAL(5,2),
    cagr_3y DECIMAL(5,2),
    cagr_5y DECIMAL(5,2),
    volatility DECIMAL(5,2),
    avg_pe DECIMAL(6,2),
    avg_pb DECIMAL(6,2),
    index_level INT,
    risk_level VARCHAR(20),
    risk_score INT,
    return_category VARCHAR(20),
    risk_adjusted_return DECIMAL(6,3),
    valuation_score DECIMAL(8,2)
);

-- 4️⃣ Insert NSE Index Data
INSERT INTO nse_indices
(index_name, market_cap_category, cagr_1y, cagr_3y, cagr_5y,
 volatility, avg_pe, avg_pb, index_level, risk_level,
 risk_score, return_category, risk_adjusted_return, valuation_score)
VALUES
('NIFTY 50','Large Cap',18.2,14.6,13.9,12.8,22.4,3.8,21750,'High',3,'Moderate',1.086,85.12),
('NIFTY NEXT 50','Large Cap',20.5,16.9,15.2,14.6,26.1,4.2,61250,'High',3,'High',1.041,109.62),
('NIFTY MIDCAP 100','Mid Cap',24.9,20.1,18.5,18.1,31.4,5.3,49250,'High',3,'Very High',1.022,166.42),
('NIFTY MIDCAP 150','Mid Cap',23.8,19.5,17.9,17.4,30.2,5.1,18940,'High',3,'High',1.028,154.02),
('NIFTY SMALLCAP 100','Small Cap',28.1,23.5,21.2,22.7,37.4,6.6,14350,'Very High',4,'Excellent',0.933,246.84),
('NIFTY SMALLCAP 250','Small Cap',26.9,22.1,20.3,21.8,35.9,6.3,11860,'Very High',4,'Excellent',0.931,226.17),
('NIFTY MICROCAP 250','Micro Cap',31.8,26.4,23.7,27.6,42.5,7.8,16230,'Extreme',5,'Excellent',0.859,331.50),
('NIFTY BANK','Sectoral Large Cap',16.1,12.9,11.8,14.2,18.6,2.9,46250,'Medium',2,'Moderate',0.831,53.94),
('NIFTY FMCG','Defensive Large Cap',12.6,13.8,14.9,9.4,45.2,10.2,54280,'Low',1,'High',1.585,461.04),
('NIFTY PHARMA','Large Cap Pharma',15.4,14.1,15.6,11.2,34.8,5.9,19760,'Medium',2,'High',1.393,205.32);

-- =====================================================
-- 5️⃣ ANALYTICS QUERIES (IMPORTANT FOR INTERVIEWS)
-- =====================================================

-- 🔝 Top 5 indices by 5Y CAGR
SELECT index_name, cagr_5y
FROM nse_indices
ORDER BY cagr_5y DESC
LIMIT 5;

-- ⚠️ Risk vs Return
SELECT index_name, volatility, cagr_5y
FROM nse_indices
ORDER BY volatility DESC;

-- 🧮 Best risk-adjusted returns
SELECT index_name, risk_adjusted_return
FROM nse_indices
ORDER BY risk_adjusted_return DESC;

-- 💰 Overvalued indices (PE × PB)
SELECT index_name, valuation_score
FROM nse_indices
ORDER BY valuation_score DESC;

-- 📊 Market-cap category performance
SELECT market_cap_category,
       ROUND(AVG(cagr_5y),2) AS avg_5y_return,
       ROUND(AVG(volatility),2) AS avg_volatility
FROM nse_indices
GROUP BY market_cap_category;

-- 🛡️ Low risk vs Extreme risk
SELECT index_name, risk_level, cagr_5y, volatility
FROM nse_indices
WHERE risk_level IN ('Low','Extreme');
