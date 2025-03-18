from . import config

def charge(gast_needed):
    """가스탱크에서 필요한 GAST을 딜러에게 제공"""
    if gast_needed <= 0:
        print("⚠️ Invalid GAST amount. Must be greater than 0.")
        return

    # 🔹 가스탱크 잔액 확인
    if config.GAS_TANK_BALANCE < gast_needed:
        print(f"⚠️ Not enough GAST in Gas Tank. Available: {config.GAS_TANK_BALANCE:.2f} GAST")
        return

    # 🔹 상태 변수 업데이트
    config.GAS_TANK_BALANCE -= gast_needed
    config.DEALER_BALANCE["gast"] += gast_needed
    config.DEALER_CHARGE_BALANCE += gast_needed # 

    print(f"✅ Charged {gast_needed:.2f} GAST to the Dealer.")
    print(f"🔹 Remaining Gas Tank Balance: {config.GAS_TANK_BALANCE:.2f} GAST")
    print(f"🔹 Updated Dealer GAST Balance: {config.DEALER_BALANCE['gast']:.2f} GAST")