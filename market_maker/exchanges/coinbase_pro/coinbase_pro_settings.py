from market_maker.strategy_settings import strategy_settings

################################################################################
#                       COINBASE PRO API SETTINGS
################################################################################


coinbase_pro_settings = {

    # Market to listen to - fetch from strategy_settings
    "SYMBOL": strategy_settings["STRATEGY"]["SYMBOL"],
    # Table lenght consider each side of the table (bids > MIN_TABLE_LENGTH and asks > MIN_TABLE_LENGTH)
    "MAX_TABLE_LENGTH": 20,
    "MIN_TABLE_LENGTH": 5,
    # Coinbase's websocket is rate-limited to 1 request per 4 seconds
    "RATE_LIMIT": 3,

    "REAL": {
        # API ENDPOINT URL
        "API_URL": "https://api.pro.coinbase.com",
        # WEB SOCKET ENDPOINT URL
        "WS_URL": "wss://ws-feed.pro.coinbase.com",
        # The Coinbase Pro API requires permanent API keys.
        "API_KEY": "98aa28357ef8e3022702a0f48e26bb95",
        "API_SECRET": "MBhcVRktfgVp2gZQN1uuE7ZIF3cw2WZ5GbKFBu2klTtu4v07X9MXBKa9bvZHR2za3lzNGtxOnzCN1/aYbVC28Q==",
        "API_PASSPHRASE": "th2x23xsu3",
    },

    "SANDBOX": {
        # API ENDPOINT URL
        "API_URL": "https://api-public.sandbox.pro.coinbase.com",
        # WEB SOCKET ENDPOINT URL
        "WS_URL": "wss://ws-feed-public.sandbox.pro.coinbase.com",
        # The Coinbase Pro API requires permanent API keys.
        "API_KEY": "352160ab686f65028c6779e90253634a",
        "API_SECRET": "22vvJUTmXraAo9YSVBe0A1CkApVkOpiBIjlOTl4gNrIlV+4D7tDZ77xnORQtn8PjTjx2NTYOJcukjjLMmoLaDg==",
        "API_PASSPHRASE": "kuhkes885lr",
    },

}
