from chainalytic_viz import client, visualizer

# ENDPOINT = 'localhost:5530'
ENDPOINT = '45.76.184.255:5530'  # production

if __name__ == '__main__':
    c = client.Client(ENDPOINT)
    v = visualizer.Visualizer(c)

    check = 0

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
        v.show_stake_history(1)
