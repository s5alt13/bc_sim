from . import config

from rich.console import Console
from rich.table import Table
from rich.progress import Progress


console = Console()

def display_state():
    
    print("\n" + "=" * 50)
    print(" " * 15 + "🚀 CURRENT STATE 🚀")
    print("=" * 50)

    # Total In / Out ETH 추가
    total_in_eth = config.TOTAL_ETH_IN
    total_out_eth = config.TOTAL_ETH_OUT

    print(f"\n{'Total In ETH':<20}: {total_in_eth:.4f} ETH")
    print(f"{'Total Out ETH':<20}: {total_out_eth:.4f} ETH")

    # GAST 발행량 프로그레스 바
    supply_percentage = (config.CURRENT_SUPPLY_GAST / config.MAX_SUPPLY_GAST) * 100
    bar_length = 30  # 바 길이
    filled_length = int(bar_length * supply_percentage / 100)
    progress_bar = "█" * filled_length + "-" * (bar_length - filled_length)
    print(f"\nGAST Supply Progress: [{progress_bar}] {supply_percentage:.2f}%\n")

    # 각 엔터티별 잔액 계산
    bonding_curve_gast = config.MAX_SUPPLY_GAST - config.CURRENT_SUPPLY_GAST  # 남은 발행 가능량
    total_eth_balance = (
        config.INVESTOR_BALANCE["eth"] +
        config.RESERVE_BALANCE +
        config.TREASURY_BALANCE["eth"] +
        config.DEALER_BALANCE["eth"] +
        config.SWAP_BALANCE["eth"] + 
        config.DEALER_USED_FEE_ETH
    )
    
    total_gast_balance = (
        config.INVESTOR_BALANCE["gast"] +
        bonding_curve_gast +
        config.TREASURY_BALANCE["gast"] +
        config.REWARD_DAY_BALANCE +
        config.DEALER_BALANCE["gast"] +
        config.SWAP_BALANCE["gast"] +
        config.GAS_TANK_BALANCE
    )

    # 보유 잔액 테이블 출력
    print(f"{'Entity':<15}{'ETH Balance':>15}{'GAST Balance':>15}")
    print("=" * 50)
    print(f"{'Investor':<15}{config.INVESTOR_BALANCE['eth']:>15.4f}{config.INVESTOR_BALANCE['gast']:>15.4f}")
    print(f"{'Bonding Curve':<15}{'-':>15}{bonding_curve_gast:>15.4f}")  # 남은 발행 가능량
    print(f"{'Reserve':<15}{config.RESERVE_BALANCE:>15.4f}{'-':>15}")
    print(f"{'Treasury':<15}{config.TREASURY_BALANCE['eth']:>15.4f}{config.TREASURY_BALANCE['gast']:>15.4f}")
    print(f"{'Reward':<15}{'-':>15}{config.REWARD_DAY_BALANCE:>15.4f}")
    print(f"{'Dealer':<15}{config.DEALER_BALANCE['eth']:>15.4f}{config.DEALER_BALANCE['gast']:>15.4f}")
    print(f"{'Dealer (TX_FEE)':<15}{config.DEALER_USED_FEE_ETH:>15.4f}{'-':>15}")
    print(f"{'Swap':<15}{config.SWAP_BALANCE['eth']:>15.4f}{config.SWAP_BALANCE['gast']:>15.4f}")
    print(f"{'Gas Tank':<15}{'-':>15}{config.GAS_TANK_BALANCE:>15.4f}")
    print("=" * 50)
    print(f"{'Total Sum':<15}{total_eth_balance:>15.4f}{total_gast_balance:>15.4f}")
    print("=" * 50)