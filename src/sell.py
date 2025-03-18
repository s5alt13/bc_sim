from . import config

import pandas as pd

# 본딩 커브 데이터 로드
bc_table = pd.read_csv(config.BC_TABLE_PATH)
    
def get_sell_price(supply):
    """현재 공급량 기준으로 판매 가격을 반환"""
    global bc_table

    # 현재 공급량보다 작거나 같은 행 찾기
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
        sell_price = lower_row["Sell Price (ETH)"]
    else:
        ratio = (supply - lower_row["Cumulative Supply"]) / (upper_row["Cumulative Supply"] - lower_row["Cumulative Supply"])
        sell_price = lower_row["Sell Price (ETH)"] + ratio * (upper_row["Sell Price (ETH)"] - lower_row["Sell Price (ETH)"])

    return sell_price

def sell(gast_amount, caller="investor"): # investor가 디폴트
    """GAST를 ETH로 변환하여 판매"""
    if gast_amount <= 0:
        print("Invalid GAST amount. Must be greater than 0.")
        return

    # 현재 발행량이 0이면 판매 불가
    if config.CURRENT_SUPPLY_GAST <= 0:
        print("⚠️ No GAST available for sale.")
        return

    remaining_gast = gast_amount
    total_eth_received = 0

    while remaining_gast > 0:
        # 현재 발행량이 0이면 판매 종료
        if config.CURRENT_SUPPLY_GAST <= 0:
            print("⚠️ All GAST sold. No more available.")
            break

        process_gast = min(remaining_gast, config.GAST_UNIT_SIZE)  # 50만 GAST 단위로 판매
        current_supply = config.CURRENT_SUPPLY_GAST

        # 현재 공급량 기준으로 판매 가격 가져오기
        sell_price = get_sell_price(current_supply)

        # GAST를 ETH로 변환
        eth_received = process_gast * sell_price

        # 리저브에 남은 ETH가 부족하면 조정
        if eth_received > config.RESERVE_BALANCE:
            eth_received = config.RESERVE_BALANCE
            process_gast = eth_received / sell_price  # 판매할 GAST 조정
            #config.INVESTOR_BALANCE['gast'] += gast_amount - process_gast

        # 상태 변수 업데이트

        config.CURRENT_SUPPLY_GAST -= process_gast
        config.RESERVE_BALANCE -= eth_received

        if caller == "investor":
            config.INVESTOR_BALANCE["gast"] -= process_gast
            config.INVESTOR_BALANCE["eth"] += eth_received
            config.TOTAL_ETH_OUT += eth_received # 외부 투자자인 경우에만 사용
        elif caller == "treasury":
            config.TREASURY_BALANCE["gast"] -= process_gast
            config.TREASURY_BALANCE["eth"] += eth_received
        elif caller == "swap":
            config.SWAP_BALANCE["gast"] -= process_gast
            config.SWAP_BALANCE["eth"] += eth_received

        remaining_gast -= process_gast
        total_eth_received += eth_received

        print(f"✅ [{caller.upper()}] Sold {process_gast:.2f} GAST for {eth_received:.2f} ETH | Sell Price: {sell_price:.6f} ETH")

        # 리저브에 ETH가 더 이상 없으면 종료
        if config.RESERVE_BALANCE <= 0:
            print("⚠️ Reserve ETH depleted. Cannot process further sales.")
            break

    return total_eth_received