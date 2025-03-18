from . import config
from . import buy
from . import sell
from . import rebalance
from . import fulfill
from . import create_ua
from . import state
from . import reward
from . import swap

def main():
    while True:
        state.display_state()
        
        print("\nSelect an option:")
        print("1. Buy GAST")
        print("2. Sell GAST")
        print("3. Rebalancing")
        print("4. Fulfill the Gas Tank")
        print("5  Create User Actions")
        print("6  Reward")
        print("7. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()

        if choice == '1':
            eth_amount = float(input("Enter ETH amount to buy GAST: "))
            buy.buy(eth_amount)
            
            # 🔹 리밸런싱 여부 확인
            print("\nWould you like to perform rebalancing?")
            print("1. Rebalance Once")
            print("2. Rebalance to Max")
            print("3. No Rebalancing")
            rebalance_choice = input("Enter your choice (1/2/3): ").strip()

            if rebalance_choice == '1':
                rebalance.rebalance(1)
            elif rebalance_choice == '2':
                rebalance.rebalance(2)
            elif rebalance_choice == '3':
                print("Skipping rebalancing.")
            else:
                print("Invalid choice. Skipping rebalancing.")

        elif choice == '2':
            gast_amount = float(input("Enter GAST amount to sell: "))
            sell.sell(gast_amount)
        
        elif choice == '3':
            print("\nSelect Rebalancing Option:")
            print("1. Rebalance Once")
            print("2. Rebalance to Max")
            rebalance_option = input("Enter your choice (1/2): ").strip()
            
            if rebalance_option in ['1', '2']:
                rebalance.rebalance(int(rebalance_option))
            else:
                print("Invalid option. Returning to main menu.")
        
        elif choice == '4':
            print("\n🔹 Fulfill Gas Tank")
            print("Enter a positive value to Deposit GAST into the gas tank.")
            print("Enter a negative value to Withdraw GAST from the gas tank.")
            
            gast_amount = float(input("Enter GAST amount: "))
            fulfilled_gast = fulfill.fulfill(gast_amount)
            
            if gast_amount > 0:
                print(f"✅ Deposited {fulfilled_gast:.2f} GAST into the Gas Tank.")
            else:
                print(f"✅ Withdrawn {abs(fulfilled_gast):.2f} GAST from the Gas Tank.")

        elif choice == '5':
            num_ua = int(input("Enter the number of User Actions to create: "))
            print(f"✅ Creating {num_ua} User Actions...")

            # User Actions 생성 및 처리 (GAST이 charge됨)
            create_ua.create_ua(num_ua)

            # 현재 딜러가 보유한 GAST 잔액 확인 (스왑 가능량)
            available_gast = config.DEALER_CHARGE_BALANCE

            if available_gast <= 0:
                print("⚠️ No GAST available for swap. Skipping swap process.")
                continue

            # 스왑 여부 확인
            state.display_state()
            print(f"\n🔹 {available_gast:.2f} GAST is available for swap.")
            print("1. Do not swap")
            print("2. Swap GAST for ETH")
            swap_choice = input("Enter your choice (1/2): ").strip()

            if swap_choice == '1':
                print("⏭️ Skipping swap process.")
                continue
            elif swap_choice == '2':
                swap_percentage = float(input("Enter percentage of GAST to swap for ETH (0-100%): ").strip())

                if swap_percentage <= 0 or swap_percentage > 100:
                    print("⚠️ Invalid percentage! Please enter a value between 0 and 100.")
                    continue

                # swap 호출 (퍼센트 값만 전달)
                swap.swap(swap_percentage)
            else:
                print("⚠️ Invalid choice! Returning to main menu.")

        elif choice == '6':
            print("\n🔹 Rewards Distribution")
            print("This process allocates funds from Treasury to the Reward Pool.")
            print("Enter the number of hours for reward distribution.")
            print("Example: 1 DAY = 24, 1 Month = 24 * 30 = 720\n")

            hours = int(input("Enter the number of hours to distribute rewards: "))
            print(f"✅ Distributing rewards for {hours} hours...")

            reward.reward(hours)
            state.display_state()

        elif choice == '7':
            print("Exiting simulation...")
            state.display_state()
            break
        
        else:
            print("Invalid choice! Please choose again.")

if __name__ == "__main__":
    main()