from . import config

def adjust_reward():
    """하루 보상량을 조정하고 시간별 보상을 계산"""
    print("\n🔄 Adjusting Reward Allocation...")

    # 🔹 트레저리 GAST의 80%를 보상 예산으로 설정
    total_treasury_gast = config.TREASURY_BALANCE["gast"]
    reward_budget = (config.REWARD_RATIO / 100) * total_treasury_gast

    if reward_budget <= 0:
        print("⚠️ Not enough GAST in Treasury for rewards.")
        return

    # 🔹 24개월(730일) 동안 지급될 하루 보상량 계산
    daily_reward = reward_budget / (config.REWARD_BUDGIT_PERIOD)

    # 🔹 하루 보상을 24시간으로 나누어 시간별 보상량 설정
    hourly_reward = daily_reward / 24

    # 🔹 보상량 업데이트
    config.REWARD_DAY_BALANCE += daily_reward
    config.TREASURY_BALANCE['gast'] -= daily_reward

    config.REWARD_HOUR_BALANCE = hourly_reward
    config.TIME_COUNT = 24  # 24시간 초기화
    
    print(f"✅ Updated Reward Allocation: {daily_reward:.2f} GAST/day, {hourly_reward:.2f} GAST/hour")


def reward(hours):
    """입력된 시간 단위만큼 보상을 지급"""
    global config

    for _ in range(hours):

        # 🔹 하루가 완료되거나, 리워드 잔고가 부족하면 보상 조정
        if config.TIME_COUNT == 0 or config.REWARD_DAY_BALANCE <= 0:
            adjust_reward()

        if config.REWARD_HOUR_BALANCE <= 0:
            print("⚠️ No rewards available for this hour.")
            return
        
        # 🔹 보상을 지급하기 전에 REWARD_DAY_BALANCE에서 차감
        config.REWARD_DAY_BALANCE -= config.REWARD_HOUR_BALANCE
        config.DEALER_BALANCE['gast'] += config.REWARD_HOUR_BALANCE  # 딜러 보상 업데이트
        config.DEALER_REWARD_BALANCE += config.REWARD_HOUR_BALANCE # 보상만 관리하는 변수 업데이트

        # 🔹 시간 카운트 감소
        config.TIME_COUNT -= 1

        # print(f"✅ Hour {_+1}: Distributed {config.REWARD_HOUR_BALANCE:.2f} GAST to the Dealer.") 


