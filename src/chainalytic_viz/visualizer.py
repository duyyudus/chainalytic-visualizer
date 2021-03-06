import os
from datetime import datetime
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

from .client import Client


class Visualizer(object):
    FIRST_BH = 7597365

    def __init__(self, client: Client):
        super(Visualizer, self).__init__()
        self.client = client
        self.stake_history_data_csv = Path(os.getcwd(), 'stake_history.csv').as_posix()
        self.stake_top100_csv = Path(os.getcwd(), 'stake_top100.csv').as_posix()

    def fetch_stake_history_data(self, height: int):
        r = self.client.get_staking_info(height)

        ts = int(r["total_staking"])
        tus = int(r["total_unstaking"])
        tsw = r["total_staking_wallets"]
        tusw = r["total_unstaking_wallets"]
        t = r["timestamp"] / 10 ** 6
        d = datetime.fromtimestamp(t).strftime('%m-%d')
        return [height, ts, tus, tsw, tusw, d]

    def fetch_stake_top100(self):
        r = self.client.latest_stake_top100()

        if 'wallets' in r:
            return [(i + 1, v) for i, v in enumerate(r['wallets'].values())]
        else:
            return []

    def show_stake_history(self, from_bh: int = None, to_bh: int = None, fetch: bool = 1):
        if fetch:
            latest_bh = self.client.last_block_height('stake_history')
            from_bh = from_bh if from_bh else Visualizer.FIRST_BH
            to_bh = to_bh if to_bh else latest_bh

            records = []
            step = 43200
            print(f'Step: {step}')
            for bh in range(from_bh, to_bh + 1, step):
                row = self.fetch_stake_history_data(bh)
                records.append(row)

            df = pd.DataFrame(
                records,
                columns=(
                    'height',
                    'total_staking',
                    'total_unstaking',
                    'total_staking_wallets',
                    'total_unstaking_wallets',
                    'date',
                ),
            )
            df.to_csv(self.stake_history_data_csv, index=False)

        df = pd.read_csv(self.stake_history_data_csv)
        # print(df)

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(2, 1, 1)
        ax2 = fig1.add_subplot(2, 1, 2)
        ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
        ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        fig2 = plt.figure()
        ax3 = fig2.add_subplot(2, 1, 1)
        ax4 = fig2.add_subplot(2, 1, 2)

        df.plot(
            kind='line',
            x='date',
            y='total_staking',
            ax=ax1,
            title='Total ICX being staked (not in unlock period)',
            grid=1,
        )
        df.plot(
            kind='line',
            x='date',
            y='total_unstaking',
            color='orange',
            ax=ax2,
            title='Total ICX in unlock period',
            grid=1,
        )

        df.plot(
            kind='line',
            x='date',
            y='total_staking_wallets',
            ax=ax3,
            title='Total wallets with ICX being staked',
            grid=1,
        )
        df.plot(
            kind='line',
            x='date',
            y='total_unstaking_wallets',
            color='orange',
            ax=ax4,
            title='Total wallets with ICX in unlock period',
            grid=1,
        )

        xticks = list(range(0, df.shape[0], df.shape[0] // 8))
        xticklabels = [df['date'][i] for i in xticks]

        ax1.set_xlabel('Date')
        ax1.set_ylabel('ICX')
        ax1.set_xticks(xticks)
        ax1.set_xticklabels(xticklabels)
        ax2.set_xlabel('Date')
        ax2.set_ylabel('ICX')
        ax2.set_xticks(xticks)
        ax2.set_xticklabels(xticklabels)

        ax3.set_xlabel('Date')
        ax3.set_ylabel('Addresses')
        ax3.set_xticks(xticks)
        ax3.set_xticklabels(xticklabels)
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Addresses')
        ax4.set_xticks(xticks)
        ax4.set_xticklabels(xticklabels)

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.2, hspace=0.3)

        plt.show()

    def show_stake_top100_distribution(self, cap_stake_amount: int = 10000000, fetch: bool = 1):
        if fetch:
            records = self.fetch_stake_top100()
            df = pd.DataFrame(records, columns=('position', 'stake_amount',))
            df.to_csv(self.stake_top100_csv, index=False)

        df = pd.read_csv(self.stake_top100_csv)
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1, 1, 1)
        ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))

        df.plot(
            kind='bar',
            x='position',
            y='stake_amount',
            ax=ax1,
            title='Top-100 wallets by staked amount',
            grid=1,
        )
        top_stake_amount = int(records[0][1])
        top_stake_amount = (
            top_stake_amount if top_stake_amount >= cap_stake_amount else cap_stake_amount
        )
        xticks = list(range(0, df.shape[0], df.shape[0] // 10))
        yticks = list(range(0, top_stake_amount, top_stake_amount // 10))
        xticklabels = [df['position'][i] for i in xticks]

        ax1.set_xlabel('Wallet position, from top-1 to top-100')
        ax1.set_ylabel('ICX')
        ax1.set_xticks(xticks)
        ax1.set_yticks(yticks)
        ax1.set_xticklabels(xticklabels)

        plt.show()
