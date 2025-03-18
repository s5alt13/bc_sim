from . import config
import pandas as pd
from src.sell import sell 

# 본딩 커브 데이터 로드
bc_table = pd.read_csv(config.BC_TABLE_PATH)

def get_buy_price(supply):
    """현재 공급량 기준으로 Buy Price 반환"""
    lower_rows = bc_table[bc_table["Cumulative Supply"] <= supply]
    if lower_rows.empty:
        lower_row = bc_table.iloc[0]
    else:
        lower_row = lower_rows.iloc[-1]

    upper_rows = bc_table[bc_table["Cumulative Supply"] > supply]
    if upper_rows.empty:
        upper_row = bc_table.iloc[-1]
    else:
        upper_row = upper_rows.iloc[0]

    # 보간 계산
    if lower_row["Cumulative Supply"] == upper_row["Cumulative Supply"]:
        buy_price = lower_row["Buy Price (ETH)"]
    else:
        ratio = (supply - lower_row["Cumulative Supply"]) / (
            upper_row["Cumulative Supply"] - lower_row["Cumulative Supply"]
        )
        buy_price = lower_row["Buy Price (ETH)"] + ratio * (
            upper_row["Buy Price (ETH)"] - lower_row["Buy Price (ETH)"]
        )

    return buy_price


def swap(swap_percentage):
    """딜러의 GAST을 ETH로 스왑하는 함수"""

    # 스왑 리밸런싱 검사
    swap_rebalance() # 실제 구현할 떄는 좀 비효율적인 루틴 같은데.. 가스비가 올라감

    # 스왑할 GAST 계산
    swap_gast_amount = (swap_percentage / 100) * config.DEALER_CHARGE_BALANCE

    if swap_gast_amount <= 0:
        print("⚠️ Swap amount is too small. Skipping swap process.")
        return

    # 현재 Buy Price 가져오기 (현재 발행량 기준)
    current_supply = config.CURRENT_SUPPLY_GAST
    buy_price = get_buy_price(current_supply)

    # 스왑할 ETH 계산
    eth_received = swap_gast_amount * buy_price

    # 스왑 가능 여부 확인 (SWAP_BALANCE[eth]보다 크면 안 됨)
    # TODO: 잔액보다 클 경우 (ua를 너무 많이 생성한 경우) 대응하는 로직이 필요함.
    if eth_received > config.SWAP_BALANCE["eth"]:
        eth_received = config.SWAP_BALANCE["eth"]
        swap_gast_amount = eth_received / buy_price  # 스왑할 GAST 조정

    if eth_received <= 0:
        print("⚠️ Not enough ETH in swap pool. Swap cancelled.")
        return

    # 상태 업데이트
    config.DEALER_CHARGE_BALANCE -= swap_gast_amount
    config.DEALER_BALANCE["gast"] -= swap_gast_amount
    config.DEALER_BALANCE["eth"] += eth_received

    # sell curve에 넣어서 ETH만 보유하고 있음. 
    config.SWAP_BALANCE["eth"] -= eth_received  
    config.SWAP_BALANCE["gast"] += swap_gast_amount

    # 결과 출력
    print(f"✅ Swapped {swap_gast_amount:.2f} GAST for {eth_received:.6f} ETH")
    print(f"🔹 Updated Dealer GAST Balance: {config.DEALER_CHARGE_BALANCE:.2f}")
    print(f"🔹 Updated Dealer ETH Balance: {config.DEALER_BALANCE['eth']:.6f}")
    print(f"🔹 Updated Swap Pool ETH: {config.SWAP_BALANCE['eth']:.6f}")
    print(f"🔹 Updated Swap Pool GAST: {config.SWAP_BALANCE['gast']:.2f}")

    # **Swap 후 자동으로 Sell 실행**
    # 스왑 잔액의 Gast만 사용하기 때문에 swap_rebalance에는 영향을 미치지 않음)
    if config.SWAP_BALANCE["gast"] > 0:
        print(f"\n🔄 Automatically selling {config.SWAP_BALANCE['gast']:.2f} GAST from Swap Pool...")
        sell(config.SWAP_BALANCE["gast"], caller="swap")

def swap_rebalance():
    """SWAP_BALANCE이 임계치보다 낮으면 트레저리에서 ETH를 보충"""

    treasury_eth = config.TREASURY_BALANCE["eth"]
    swap_eth = config.SWAP_BALANCE["eth"]

    # 리밸런싱 트리거 기준
    swap_target = (config.SWAP_RATIO_THRESHOLD / 100) * treasury_eth
    swap_lower_bound = swap_target - ((config.SWAP_RANGE / 100) * treasury_eth)

    if swap_eth >= swap_lower_bound:
        return  # 스왑 풀에 충분한 ETH가 있으면 리밸런싱 필요 없음

    # 부족한 ETH 보충 (5% 목표치까지)
    eth_to_transfer = min(swap_target, treasury_eth)
    config.TREASURY_BALANCE["eth"] -= eth_to_transfer
    config.SWAP_BALANCE["eth"] += eth_to_transfer

    print(f"🔄 Swap Rebalanced: {eth_to_transfer:.6f} ETH moved from Treasury to Swap Pool.")
    print(f"🔹 New Swap Pool ETH Balance: {config.SWAP_BALANCE['eth']:.6f}")