"""
SQL queries for Dune Analytics to retrieve lending protocol data.
These queries can be used with the DuneLendingProtocols class to create custom queries.
"""

# Query to get all major lending protocols across chains with their details
LENDING_PROTOCOLS_OVERVIEW_SQL = """
SELECT 
  protocol_name,
  chain,
  protocol_version,
  launch_date,
  TVL_USD as total_value_locked_usd,
  daily_active_users,
  daily_supply_volume_usd,
  daily_borrow_volume_usd,
  website_url
FROM 
  lending_protocols
WHERE
  1=1
  {% if defined(Chain) %}
  AND chain = '{{Chain}}'
  {% endif %}
ORDER BY
  TVL_USD DESC
"""

# Query to get TVL data for lending protocols
LENDING_PROTOCOLS_TVL_SQL = """
SELECT 
  protocol_name,
  chain,
  date_trunc('day', block_time) as day,
  asset_symbol,
  SUM(supply_balance_usd) as total_supply_usd,
  SUM(borrow_balance_usd) as total_borrow_usd,
  SUM(supply_balance_usd - borrow_balance_usd) as tvl_usd
FROM 
  lending_daily_balances
WHERE
  block_time >= NOW() - INTERVAL '30 days'
  {% if defined(ProtocolName) %}
  AND protocol_name = '{{ProtocolName}}'
  {% endif %}
GROUP BY
  protocol_name, chain, day, asset_symbol
ORDER BY
  day DESC, tvl_usd DESC
"""

# Query to get current lending and borrowing rates for protocols
LENDING_RATES_SQL = """
SELECT 
  protocol_name,
  chain,
  asset_symbol,
  supply_rate_apy,
  borrow_rate_apy,
  updated_at
FROM 
  lending_current_rates
WHERE
  1=1
  {% if defined(ProtocolName) %}
  AND protocol_name = '{{ProtocolName}}'
  {% endif %}
  {% if defined(Asset) %}
  AND asset_symbol = '{{Asset}}'
  {% endif %}
ORDER BY
  protocol_name, asset_symbol
"""

# Query to get the top lending protocols by volume in the last 7 days
TOP_LENDING_PROTOCOLS_SQL = """
SELECT 
  protocol_name,
  chain,
  SUM(supply_volume_usd + borrow_volume_usd) as total_volume_usd,
  COUNT(DISTINCT user_address) as unique_users,
  AVG(supply_rate_apy) as avg_supply_apy,
  AVG(borrow_rate_apy) as avg_borrow_apy
FROM 
  lending_daily_activities
WHERE
  block_time >= NOW() - INTERVAL '7 days'
GROUP BY
  protocol_name, chain
ORDER BY
  total_volume_usd DESC
LIMIT 20
"""

# Query to get historical borrowing and lending volumes for a specific protocol
PROTOCOL_HISTORICAL_VOLUMES_SQL = """
SELECT 
  date_trunc('day', block_time) as day,
  asset_symbol,
  SUM(supply_volume_usd) as daily_supply_volume_usd,
  SUM(borrow_volume_usd) as daily_borrow_volume_usd
FROM 
  lending_daily_activities
WHERE
  protocol_name = '{{ProtocolName}}'
  AND block_time >= NOW() - INTERVAL '{{Days}}' day
GROUP BY
  day, asset_symbol
ORDER BY
  day DESC, asset_symbol
"""

# Query to find lending opportunities with the highest supply APY
BEST_LENDING_OPPORTUNITIES_SQL = """
SELECT 
  protocol_name,
  chain,
  asset_symbol,
  supply_rate_apy,
  borrow_rate_apy,
  updated_at,
  TVL_USD as total_value_locked_usd
FROM 
  lending_current_rates lcr
JOIN
  lending_protocols lp ON lcr.protocol_name = lp.protocol_name AND lcr.chain = lp.chain
WHERE
  supply_rate_apy > 0
  {% if defined(MinTVL) %}
  AND TVL_USD >= {{MinTVL}}
  {% endif %}
ORDER BY
  supply_rate_apy DESC
LIMIT 50
""" 