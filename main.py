from chainalytic_viz import client, visualizer

# ENDPOINT = 'localhost:5530'
# ENDPOINT = '45.76.184.255:5530'  # app
# ENDPOINT = '45.76.184.255:5531'  # app-dev
# ENDPOINT = '140.82.11.203:5531'  # production chainalytic-dev
ENDPOINT = '140.82.11.203:5530'  # production chainalytic
# ENDPOINT = '35.240.229.245:5530'  # dev

if __name__ == '__main__':
    c = client.Client(ENDPOINT)
    v = visualizer.Visualizer(c)

    check = 9

    if check == 0:
        c.last_block_height('stake_history')
    elif check == 1:
        c.get_staking_info_last_block()
    elif check == 2:
        c.get_staking_info(12000000)
    elif check == 3:
        c.latest_unstake_state()
    elif check == 4:
        c.latest_stake_top100()
    elif check == 5:
        c.recent_stake_wallets()
    elif check == 6:
        c.abstention_stake()
    elif check == 7:
        c.funded_wallets(min_balance=1)
    elif check == 8:
        c.passive_stake_wallets(max_inactive_duration=40000)
    elif check == 9:
        v.show_stake_history(from_bh=7841000, fetch=1)
        # v.show_stake_history(from_bh=None, fetch=1)
