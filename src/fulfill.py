from . import config

def fulfill(gast_amount):
    """가스 탱크를 채우거나 출금하는 함수"""
    
    if gast_amount == 0:
        print("⚠️ Invalid amount. Must be non-zero.")
        return 0

    if gast_amount > 0:
        # 충전 로직 (양수 입력)
        fulfilled_gast = min(gast_amount, config.INVESTOR_BALANCE['gast'])

        if fulfilled_gast <= 0:
            print("⚠️ No GAST available to fulfill gas tank.")
            return 0

        # 상태 변수 업데이트
        config.INVESTOR_BALANCE['gast'] -= fulfilled_gast  
        config.GAS_TANK_BALANCE += fulfilled_gast  

        print(f"✅ Gas Tank filled with {fulfilled_gast:.2f} GAST.")

    else:
        # 출금 로직 (음수 입력)
        withdraw_gast = min(abs(gast_amount), config.GAS_TANK_BALANCE)

        if withdraw_gast <= 0:
            print("⚠️ Not enough GAST in Gas Tank to withdraw.")
            return 0

        # 상태 변수 업데이트
        config.GAS_TANK_BALANCE -= withdraw_gast  
        config.INVESTOR_BALANCE['gast'] += withdraw_gast 

        print(f"✅ Withdrawn {withdraw_gast:.2f} GAST from Gas Tank.")

    return gast_amount