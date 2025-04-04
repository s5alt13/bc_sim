from . import config
from . import buy  

def rebalance(option):
    """리밸런싱 실행 (RTR 기준 적용)"""

    print("\n🔄 Checking Rebalancing Conditions...")

    # 리밸런싱 파라미터 (RTR 기반)
    RTR_THRESHOLD = config.RTR_THRESHOLD  # 리밸런싱 트리거 기준 (%)
    RTR_RANGE = config.RTR_RANGE  # 리밸런싱 허용 범위 (%)

    # 현재 트레저리 ETH 잔고 확인
    treasury_eth = config.TREASURY_BALANCE["eth"]
    if treasury_eth == 0:
        print("⚠️ Not enough ETH in Treasury for rebalancing.")
        return

    # 현재 트레저리 ETH 비율 계산
    total_eth = treasury_eth + config.RESERVE_BALANCE  # 리저브 포함 (리저브 ETH는 변동 없음)
    treasury_ratio = (treasury_eth / total_eth) * 100 if total_eth > 0 else 0
    initial_treasury_ratio = treasury_ratio  # 초기 RTR 저장

    # 리밸런싱 필요 여부 확인
    if treasury_ratio < RTR_THRESHOLD:
        print(f"✅ No rebalancing needed. Current Treasury ETH Ratio: {treasury_ratio:.2f}%")
        return

    print(f"🔹 Initial RTR: {initial_treasury_ratio:.2f}% (Target: {config.RTR_THRESHOLD:.2f}%)")
    
    # 리밸런싱 수행
    while treasury_ratio >= RTR_THRESHOLD:
        eth_to_use = ((treasury_ratio - RTR_THRESHOLD) / 100) * total_eth  
        eth_to_use = min(eth_to_use, treasury_eth)  # 트레저리 보유 ETH를 초과하지 않도록 제한

        # ETH 사용량이 10 ETH 미만이면 리밸런싱 중단
        if eth_to_use < 10:
            print(f"⚠️ Rebalancing stopped: ETH to use ({eth_to_use:.4f} ETH) is too small.")
            return

        print(f"🔄 Using {eth_to_use:.4f} ETH from Treasury to buy GAST...")
        buy.buy(eth_to_use, from_treasury=True)  # 트레저리에서 구매 실행

        # 업데이트된 잔고 반영
        treasury_eth = config.TREASURY_BALANCE["eth"]
        treasury_gast = config.TREASURY_BALANCE["gast"]
        total_eth = treasury_eth + config.RESERVE_BALANCE
        treasury_ratio = (treasury_eth / total_eth) * 100 if total_eth > 0 else 0

        print(f"🔹 Updated RTR: {treasury_ratio:.2f}% | Treasury ETH: {treasury_eth:.4f} | Treasury GAST: {treasury_gast:.2f}")

        if option == 1:  # 한 번만 실행하는 경우 종료
            break

        if treasury_ratio < (RTR_THRESHOLD - RTR_RANGE):  # 45% 이하가 되면 중단
            print(f"✅ Stopping Rebalancing as RTR reached {treasury_ratio:.2f}% (Below {RTR_THRESHOLD - RTR_RANGE}%)")
            break