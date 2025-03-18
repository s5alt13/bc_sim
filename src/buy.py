from . import config

import pandas as pd
import numpy as np

# 본딩 커브 데이터 로드
bc_table = pd.read_csv(config.BC_TABLE_PATH)

def get_buy_price(supply):
    """현재 공급량 기준으로 구매 가격과 스프레드를 반환"""
    global bc_table

    # 현재 공급량보다 작거나 같은 행 찾기
    lower_rows = bc_table[bc_table["Cumulative Supply"] <= supply]

    if lower_rows.empty:
        # lower_row가 없으면 테이블 첫 번째 값 사용 (supply가 0일 경우)
        lower_row = bc_table.iloc[0]
    else:
        lower_row = lower_rows.iloc[-1]

    upper_rows = bc_table[bc_table["Cumulative Supply"] > supply]

    if upper_rows.empty:
        # upper_row가 없으면 마지막 행 사용
        upper_row = bc_table.iloc[-1]
    else:
        upper_row = upper_rows.iloc[0]

    # 보간 계산
    if lower_row["Cumulative Supply"] == upper_row["Cumulative Supply"]:
        buy_price = lower_row["Buy Price (ETH)"]
        spread = lower_row["Spread"]
    else:
        ratio = (supply - lower_row["Cumulative Supply"]) / (upper_row["Cumulative Supply"] - lower_row["Cumulative Supply"])
        buy_price = lower_row["Buy Price (ETH)"] + ratio * (upper_row["Buy Price (ETH)"] - lower_row["Buy Price (ETH)"])
        spread = lower_row["Spread"] + ratio * (upper_row["Spread"] - lower_row["Spread"])

    return buy_price, spread

def buy(eth_amount, from_treasury=False):
    """ETH를 GAST로 변환하여 구매 (트레저리 또는 외부 사용자가 호출 가능)"""
    if eth_amount <= 0:
        print("Invalid ETH amount. Must be greater than 0.")
        return

    # 최대 공급량 도달 여부 확인
    if config.CURRENT_SUPPLY_GAST >= config.MAX_SUPPLY_GAST:
        print("⚠️ MAX SUPPLY reached. No more GAST can be minted.")
        return

    # 트레저리에서 구매하는 경우, ETH 차감
    if from_treasury:
        if config.TREASURY_BALANCE["eth"] < eth_amount:
            print("⚠️ Not enough ETH in Treasury for rebalancing.")
            return
        config.TREASURY_BALANCE["eth"] -= eth_amount  # 트레저리 ETH 차감

    remaining_eth = eth_amount
    total_gast_minted = 0

    while remaining_eth > 0:
        # 최대 공급량 도달 시 중단
        if config.CURRENT_SUPPLY_GAST >= config.MAX_SUPPLY_GAST:
            print("⚠️ MAX SUPPLY reached during the process. Stopping further purchases.")
            break

        process_eth = min(remaining_eth, config.ETH_UNIT_SIZE)  # 10ETH 단위로 구매
        current_supply = config.CURRENT_SUPPLY_GAST

        # 현재 공급량 기준으로 구매 가격과 스프레드 가져오기
        buy_price, spread = get_buy_price(current_supply)

        # ETH를 GAST로 변환
        gast_minted = process_eth / buy_price

        # 최대 공급량 초과 체크
        if config.CURRENT_SUPPLY_GAST + gast_minted > config.MAX_SUPPLY_GAST:
            gast_minted = config.MAX_SUPPLY_GAST - config.CURRENT_SUPPLY_GAST
            process_eth = gast_minted * buy_price  # 사용된 ETH 재조정
            # TODO: eth_amount 만큼 들어온 상태에서 process_eth 만큼 처리하면 남은 건 다시 반환해줘야 함. 
            config.INVESTOR_BALANCE['eth'] += eth_amount - process_eth
            config.TOTAL_ETH_IN += eth_amount - process_eth

        # 상태 변수 업데이트
        config.CURRENT_SUPPLY_GAST += gast_minted

        # 트레저리가 아닌 외부에서 구매한 경우만 ETH_IN 증가
        if not from_treasury:
            config.TOTAL_ETH_IN += process_eth  
            config.INVESTOR_BALANCE['gast'] += gast_minted

        # 리저브 & 트레저리 분배 (트레저리에서 구매한 경우에도 동일)
        reserve_share = process_eth * (1 - spread)
        treasury_share = process_eth * spread

        config.RESERVE_BALANCE += reserve_share
        config.TREASURY_BALANCE["eth"] += treasury_share

        # 트레저리가 구매한 경우, GAST 증가
        if from_treasury:
            config.TREASURY_BALANCE["gast"] += gast_minted  # 트레저리 GAST 증가

        remaining_eth -= process_eth
        total_gast_minted += gast_minted

        # print(f"✅ Bought {gast_minted:.2f} GAST for {process_eth:.2f} ETH | Buy Price: {buy_price:.6f} ETH")

    return total_gast_minted