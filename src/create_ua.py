
from . import config
from . import charge  
from src.buy import get_buy_price  

import pandas as pd

def create_ua(num_ua):
    """User Action을 생성하고, 해당 비용을 ETH에서 차감 후 GAST으로 변환"""

    if num_ua <= 0:
        print("❌ Invalid number of User Actions. Must be greater than 0.")
        return

    # 총 ETH 소모량 계산
    total_eth_cost = num_ua * config.AVERAGE_GAS_COST

    # 현재 GAST 가격 가져오기 (발행량 기준)
    current_supply = config.CURRENT_SUPPLY_GAST
    buy_price, _ = get_buy_price(current_supply)  # 현재 가격 조회

    # GAST 변환량 계산
    gast_needed = total_eth_cost / buy_price  

    # 가스 탱크 잔액 확인 (초과 여부 검사)
    if gast_needed > config.GAS_TANK_BALANCE:
        print(f"⚠️ Not enough GAST in Gas Tank! Required: {gast_needed:.2f}, Available: {config.GAS_TANK_BALANCE:.2f}")
        return  

    # Dealer의 ETH 잔액 차감
    config.DEALER_BALANCE["eth"] -= total_eth_cost

    # 딜러가 수수료에 사용한 ETH 
    config.DEALER_USED_FEE_ETH += total_eth_cost


    # 결과 출력
    print(f"✅ Created {num_ua} User Actions.")
    print(f"🔹 Total ETH Cost: {total_eth_cost:.6f} ETH")
    print(f"🔹 GAST Used: {gast_needed:.2f} GAST")

    # charge.py의 charge(amount) 호출하여 GAST 차감
    charge.charge(gast_needed)