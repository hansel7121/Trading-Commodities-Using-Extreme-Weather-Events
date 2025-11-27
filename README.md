# Seasonal Trading (Trading Crop and Animal Commodities Based on Extreme Weather Events)

This repository contains a backtesting framework for trading crop commodities based on extreme weather events that directly affect the growth of the crop.

# Contributors

- Hansel Chen
- Ian Liu

# Method

Crops tend to surge in price when supply is shocked by environmental factors. With global warming becoming a bigger issue than ever before, we decided to capitalize on these extreme weather conditions becoming more common. This strategy involves buying crops after their region experiences extreme temperatures that are unsustainable for the growth of the crop during its harvesting and growing seasons. We will then hold for a period of time and wait for the market to react back, and we will then liquidate our positions, hopefully with a profit.

# Key Features

- Uses NASA's satellite data to extract daily temperature highs and lows for the past decade. Location/region/elevation is fully customizable to match the locations the crops are grown in.
- Based on a crop's optimal temperature, it generates buy signals for extreme temperature deviations during critical time periods of the year (harvesting/flowering times).
- Portfolio equity curve visualization
- Accounts for rolling costs in equity visualization
- Optimizes holding period of contracts

# Usage

Consult presentation.ipynb for the full rundown of our exploration into this strategy.

cropname_data.py is how we scraped data from NASA's API. cropname.py is how each crop performs using our method. This is applicable for all crops that are sensitive to changes in temperature. Winter Wheat, for example, does not work in this model as it is considered a "zombie corpse" and doesn't die easily.

cropname_roll_yield runs the test but with rolling costs
