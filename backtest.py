import pandas as pd
import numpy as np
from io import StringIO
from AlgorithmImports import *

class RedditStockSentiment(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021,3, 1)  # Set Start Date
        self.SetEndDate(2021, 6, 18) #Set End Date
        self.SetCash(100000)  # Set Strategy Cash
        self.tickers = ["CLNE", "AMC","BB","PLTR","NVDA","TSLA","CLOV","GME","AMD","CLF","UWMC","WKHS","AAPL","AMZN","TLRY","PRPL","SOFI","NIO","DKNG","NNDM","ET","CRSR","ITUB","ASO","BABA","GLD","ARVL","WISH","VIAC","SNDL","GOEV","WOOF","SENS","NET","ME","HUYA","DIS","GOOGL","MSFT","SPCE","TIL","RKT","JPM","EM","APP","LEV","F","SQQQ","TQQQ","CVAC","ARKK","SLV","FB","NOK","OCGN","SQ","XPEV","JD","VZIO","XLF","HYLN","GE","NFLX","ROPE","WEN","FSR","TLT","SPOT","MT","TTD","BA","SI","FUBO","PYPL","WFC","ENPH","BAC","XOM","INTC","PSFE","TAL","ZM","COIN","TRCH","SCR","ROOT","QS","SKLZ","ATOS","GEO","UVXY","SHOP","RBLX","DE","GM","LI","UPS","DASH","ROKU","NKLA","WTI","CHPT","SWBI","FINV","VXRT","OXY","WIT","MX","PLUG","ZNGA","TM","MARA","IDEX","ADBE","ABNB","DDS","WMT","TX","IWM","ASAN","RIOT","MVIS","MNMD","PINS","ARKF","BBY","GUSH","PENN","NNOX","STEM","BYND","LUV","NUE","IOVA","NEE","PS","MRO","OGS","RUN","XLE","FCEL","MCD","UPST","ETSY","JMIA","DIA","BNGO","SDC","EDU","UBER","ZIM","OPEN","MSOS","MOO","NKE","HD","RNG","PATH","WLK","RAIN","FCX","SNAP","CPNG","MAPS","INO","LEN","SOLO","PTON","MU","HSY"]
        self.investP = 1/len(self.tickers) #Equal weight portfolio
        self.SetWarmup(TimeSpan.FromDays(65))

        # self.Settings.RebalancePortfolioOnInsightChanges = False
        # self.Settings.RebalancePortfolioOnSecurityChanges = False
        # self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(lambda time: None))
        # self.SetPortfolioConstruction(InsightWeightingPortfolioConstructionModel(
        #                       rebalancingParam = timedelta(days = 30), 
        #                       portfolioBias = PortfolioBias.Long))
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(self.RebalanceFunction))

        for stock in self.tickers:
            self.AddEquity(stock, Resolution.Daily) #Sets resolution to hour bars
        
        self.AddRiskManagement(TrailingStopRiskManagementModel(0.08)) #Risk management
        
        self.trade = True #OnData will run when the program when the program is first executed
        
        csv = self.Download("https://raw.githubusercontent.com/sommohapatra/reddit_sentiment/main/Reddit_Sentiment_Equity_new.csv") #Downloads data
        self.df = pd.read_csv(StringIO(csv)) #Read into a dataframe
        
        self.Schedule.On(self.DateRules.EveryDay(), 
                 self.TimeRules.At(10, 30),        
                 self.runDaily) #Runs runDaily (sets self.trade to True) at 8:30am Chicago time

    def RebalanceFunction(self, time):
        # for performance only run rebalance logic once a week, monday
        if time.weekday() != 0:
            return None

    def OnData(self, data):
        algYear = self.Time.year
        algMonth = self.Time.month
        algDay = self.Time.day
        if(algYear == 2021 and algMonth == 3 and algDay == 2):
            self.MarketOrder("PYPL", 36)


    def runDaily(self):
        self.trade = True

# class PortfolioRebalanceOnCustomFuncRegressionAlgorithm(QCAlgorithm):
#     def Initialize(self):
#         ''' Initialise the data and resolution required, as well as the cash and start-end dates for your algorithm. All algorithms must initialized.'''

#         self.UniverseSettings.Resolution = Resolution.Daily

#         self.SetStartDate(2015, 1, 1)
#         self.SetEndDate(2018, 1, 1)

#         self.Settings.RebalancePortfolioOnInsightChanges = False;
#         self.Settings.RebalancePortfolioOnSecurityChanges = False;

#         self.SetUniverseSelection(CustomUniverseSelectionModel("CustomUniverseSelectionModel", lambda time: [ "AAPL", "IBM", "FB", "SPY", "AIG", "BAC", "BNO" ]))
#         self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, TimeSpan.FromMinutes(20), 0.025, None));
#         self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel(self.RebalanceFunction))
#         self.SetExecution(ImmediateExecutionModel())
#         self.lastRebalanceTime = self.StartDate

#     def RebalanceFunction(self, time):
#         # for performance only run rebalance logic once a week, monday
#         if time.weekday() != 0:
#             return None

#         if self.lastRebalanceTime == self.StartDate:
#             # initial rebalance
#             self.lastRebalanceTime = time;
#             return time;

#         deviation = 0;
#         count = sum(1 for security in self.Securities.Values if security.Invested)
#         if count > 0:
#             self.lastRebalanceTime = time;
#             portfolioValuePerSecurity = self.Portfolio.TotalPortfolioValue / count;
#             for security in self.Securities.Values:
#                 if not security.Invested:
#                     continue
#                 reservedBuyingPowerForCurrentPosition = (security.BuyingPowerModel.GetReservedBuyingPowerForPosition(
#                     ReservedBuyingPowerForPositionParameters(security)).AbsoluteUsedBuyingPower
#                                                          * security.BuyingPowerModel.GetLeverage(security)) # see GH issue 4107
#                 # we sum up deviation for each security
#                 deviation += (portfolioValuePerSecurity - reservedBuyingPowerForCurrentPosition) / portfolioValuePerSecurity;

#             # if securities are deviated 1.5% from their theoretical share of TotalPortfolioValue we rebalance
#             if deviation >= 0.015:
#                 return time
#         return None

#     def OnOrderEvent(self, orderEvent):
#         if orderEvent.Status == OrderStatus.Submitted:
#             if self.UtcTime != self.lastRebalanceTime or self.UtcTime.weekday() != 0:
#                 raise ValueError(f"{self.UtcTime} {orderEvent.Symbol}")
