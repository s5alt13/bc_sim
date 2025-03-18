import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BC_TABLE_PATH = os.path.join(BASE_DIR, "data", "bc_table.csv")

# 본딩 커브 토큰 발행량 설정 
MAX_SUPPLY_GAST = 100_000_000  # 최대 1억 개 공급 가능
CURRENT_SUPPLY_GAST = 0 # 현재 발행된 공급량

# 거래 단위 설정
ETH_UNIT_SIZE = 10  # Buy 수행 시 ETH 거래 단위 (거래 최소 단위)
GAST_UNIT_SIZE = 10_000  # Sell 수행 시 GAST 단위 (거래 최소 단위)
TOTAL_ETH_IN = 0  # 외부에서 유입된 총 ETH
TOTAL_ETH_OUT = 0  # 외부로 유출된 총 ETH (GAST 판매로 인한 ETH 반환)

# 인터페이스 잔액 상태 변수 
INVESTOR_BALANCE = {"eth": 0, "gast": 0}  # 외부 투자자 ETH 및 GAST 잔액
RESERVE_BALANCE = 0  # 리저브 ETH 잔고 
TREASURY_BALANCE = {"eth": 0, "gast": 0}  # 트레저리 ETH 및 GAST 잔액
DEALER_BALANCE = {"eth": 1000, "gast": 0}  # 트레저리 ETH 및 GAST 잔액, 초기 ETH 필요
SWAP_BALANCE = {"eth": 0, "gast": 0}  # 트레저리 ETH 및 GAST 잔액

# 리워드, 스왑은 유동적이라 따로 관리 하지 않음. 

# 리저브/트레저리 비율 (RTR)
RTR_THRESHOLD = 50  # 리밸런싱 트리거 기준 (%)
RTR_RANGE = 5  # 허용 리밸런싱 범위 (%)

# 스왑 
SWAP_RATIO_THRESHOLD = 5 # 
SWAP_RANGE = 2 

# 가스 탱크
GAS_TANK_BALANCE = 0

# User Action 설정 
AVERAGE_GAS_COST = 0.000001 # 트랜잭션 당 평균 가스 비용 몇원 수준

# 딜러 설정 
DEALER_USED_FEE_ETH = 0 # 딜러가 수수료에 소모한 금액 (일하는 데 쓴 수수료) 계속 증가만 하는 변수
DEALER_CHARGE_BALANCE = 0 # 딜러가 charge 해서 받는 것이 가능한 GAST 수량. 스왑할 때 감소
DEALER_REWARD_BALANCE = 0 # 딜러가 보상으로만 받은 금액 

# 리워드 설정
REWARD_DAY_BALANCE = 0 # 24시간에 한번씩 트레저리로부터 가져옴 
REWARD_HOUR_BALANCE = 0
REWARD_BUDGIT_PERIOD = 2 * 365 
REWARD_RATIO = 80 # 트레저리의 80%를 기준으로 계산
TIME_COUNT = 24 # 1시간에 1씩 감소