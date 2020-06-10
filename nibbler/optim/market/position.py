import numpy as np


class Position:

    positionType = "position"

    def __new__(
        cls,
        trader,
        market,
        quantity,
        entryPrice,
        leverage=1,
        reduceOnly=False
    ):
        assert leverage <= market.maxLeverage

        if trader in market.positions.keys():
            position = cls.modifyPosition(
                trader, market, quantity, entryPrice,
                leverage, reduceOnly
            )
        elif not reduceOnly:
            position = cls.newPosition(
                trader, market, quantity, entryPrice,
                leverage, reduceOnly
            )
        else:
            return None
        
        return position
    
    @staticmethod
    def weightedAverage(p1,p2,w1,w2):
        return ((p1*w1)+(p2*w2))/(w1+w2)
    
    @staticmethod
    def getEntryAndFee(entryPrice, market):
        if entryPrice is "market":
            entryPrice = market.getLatestOpenPrice()
            usedFee = market.takerFee
        else:
            usedFee = market.makerFee
        return entryPrice, usedFee

    @classmethod
    def logTradeTimestamp(cls, trader, market):
        pass

    def close(self):
        del self.market.positions[self.trader]
        del self.trader.positions[self.market]

    def getLatestFeed(self):
        currentFeed = self.market.feeds[self.market.smallestTimeframe]
        return currentFeed    
    
    def getLatestClosePrice(self):
        return self.getLatestFeed()[:, -1]
    
    def getMargin(self):
        return (self.entryPrice * self.quantity)/self.leverage
    
    def isLiquidated(self):
        '''
            when an exchange contains more than one coin
            this must be optimized
        '''
        if self.leverage == 1:
            return False 
        dollarMovement = \
            self.getLargestNegativePositionVariation() * self.quantity
        if dollarMovement >= self.getMargin():
            self.close()
            return True
        return False

    @staticmethod
    def slippage(entryPrice, market):
        NotImplemented 

    def unrealizedPNL(self):
        pass

    @classmethod
    def modifyPosition(
            cls, trader, market, quantity,
            entryPrice, leverage, reduceOnly
        ):
        # when modifying a position we need to call the logTradeTimestamp

        NotImplemented
    
    @classmethod
    def newPosition(
            cls, trader, market, quantity,
            entryPrice, leverage, reduceOnly
        ):

        if reduceOnly:
            return None

        cls.logTradeTimestamp(trader, market)

        position = object.__new__(cls)
        position.trader = trader
        position.market = market
        position.quantity = quantity
        position.leverage = leverage

        entryPrice, usedFee = cls.getEntryAndFee(entryPrice, market)
        entryPrice = cls.slippage(entryPrice, market)
        position.entryPrice = entryPrice

        # calculate the cost to the user 
        dollarCost = quantity * entryPrice
        fees = dollarCost * usedFee 
        userCost = dollarCost/leverage + fees

        if userCost > trader.balance:
            return None

        trader.balance -= userCost
        market.positions[trader] = position
        trader.positions[market] = position

        return position 

    @classmethod
    def addPosition(
            cls, currentPosition, trader, market,
            quantity, entryPrice, leverage, reduceOnly
        ):
        # get the original entry and quantity
        originalQuantity = currentPosition.quantity
        originalEntry = currentPosition.entryPrice
        # dictate on which fee to be used depending on 
        # if the order is market or limit
        entryPrice, usedFee = cls.getEntryAndFee(entryPrice, market)
        # calculate the cost to the user 
        dollarCost = quantity * entryPrice
        fees = dollarCost * usedFee 
        userCost = dollarCost/leverage + fees
        # minus it from the users current Balance
        if userCost > trader.balance:
            return currentPosition
        # if successful update the traders balance and positions
        trader.balance -= userCost
        # increment the quantity by the desired amount
        currentPosition.quantity += quantity
        # calcualte the weighted average entry price
        currentPosition.entryPrice = cls.weightedAverage(
            originalEntry, entryPrice, originalQuantity, quantity
        )
        # update the leverage used
        currentPosition.leverage = cls.weightedAverage(
            currentPosition.leverage, leverage, originalQuantity, quantity
        )
        return currentPosition

    @classmethod
    def reducePosition(
        cls, currentPosition, trader, market, quantity,
        entryPrice, leverage, reduceOnly
    ):
        if reduceOnly:
            if quantity > currentPosition.quantity:
                quantity = currentPosition.quantity
        # calculate the fees to the user
        entryPrice, usedFee = cls.getEntryAndFee(entryPrice, market)
        entryPrice = cls.slippage(entryPrice, market)
        dollarCost = quantity * entryPrice
        fees = dollarCost * usedFee 
        # this priceMovement is variable
        # priceMovement = currentPosition.entryPrice - entryPrice
        priceMovement = cls.getPriceMovement(currentPosition, entryPrice)
        originalCost = currentPosition.entryPrice * quantity
        pnl = (priceMovement*quantity) 
        totalPNL = (
            pnl + (originalCost)/currentPosition.leverage)
        trader.balance += (totalPNL-fees)
        # calculate the percentage profit and loss
        percentWL = ((originalCost + pnl)/originalCost - 1)*100
        # log whether the trade was won or lost
        if pnl <= 0:
            trader.tradesLost += 1
            trader.lossPercentages.append(percentWL)
        else:
            trader.tradesWon += 1
            trader.winPercentages.append(percentWL)
        # update the current position 
        currentPosition.quantity -= quantity
        if np.isclose(currentPosition.quantity, 0):
            currentPosition.close()
            return None
        elif currentPosition.quantity < 0:
            shortQuantity = np.abs(currentPosition.quantity)
            currentPosition.close()
            position = cls.__new__(
                cls, trader, market, shortQuantity, entryPrice,
                leverage=leverage, reduceOnly=reduceOnly
            )
            return position
        return currentPosition

    @staticmethod
    def getPriceMovement(currentPosObject, entryPrice):
        NotImplemented
    
    def getLargestPositionVariation(self):
        NotImplemented
    
    def __repr__(self):
        output = \
            "<Postion: trader=%s, market=%s-%s, entryPrice=%0.3f, quantity=%0.3f, type=%s>"
        return output%(
            self.trader.id,
            self.market.pair1,
            self.market.pair2,
            self.entryPrice,
            self.quantity,
            self.positionType
        )

    def getLargestNegativePositionVariation(self):
        return (self.entryPrice - self.market.getLatestFeed()[3])*self.quantity

# ---------------------------------------------------------------
class LongPosition(Position):

    positionType = "longPosition"

    def getLargestNegativePositionVariation(self):
        return (self.entryPrice - self.market.getLatestFeed()[3])*self.quantity

    @classmethod
    def logTradeTimestamp(cls, trader, market):
        trader.buyTimestamps[market.name].append(market.getLatestTime())

    @staticmethod
    def slippage(entryPrice, market):
        return entryPrice + entryPrice * market.slippage 

    def marketClose(self):
        quantity = self.market.positions[self.trader].quantity
        LongPosition(
            self.trader, self.market, quantity, "market", 
            self.leverage, reduceOnly=True
        )

    def unrealizedPNL(self):
        currentPrice = self.getLatestClosePrice()[4]
        priceMovement = currentPrice - self.entryPrice
        return priceMovement * self.quantity

    @staticmethod 
    def getPriceMovement(currentPosObject, entryPrice):
        return currentPosObject.entryPrice - entryPrice

    @classmethod
    def modifyPosition(cls, trader, market, quantity, entryPrice, leverage, reduceOnly):

        cls.logTradeTimestamp(trader, market)

        currentPosition = market.positions[trader]
        # if the traders position in the market is a long position
        if isinstance(currentPosition, LongPosition):
            currentPosition = cls.addPosition(
                currentPosition, trader, market, quantity,
                entryPrice, leverage, reduceOnly
            )

        elif isinstance(currentPosition, ShortPosition):
            currentPosition = cls.reducePosition(
                currentPosition, trader, market, quantity,
                entryPrice, leverage, reduceOnly 
            )
        
        return currentPosition

# ---------------------------------------------------------------
class ShortPosition(Position):

    positionType = "shortPosition"

    def getLargestNegativePositionVariation(self):
        return (self.market.getLatestFeed()[2] - self.entryPrice)*self.quantity

    @classmethod
    def logTradeTimestamp(cls, trader, market):
        trader.sellTimestamps[market.name].append(market.getLatestTime())

    @staticmethod
    def slippage(entryPrice, market):
        return entryPrice - entryPrice * market.slippage 
    
    def unrealizedPNL(self):
        currentPrice = self.getLatestClosePrice()[4]
        priceMovement = self.entryPrice - currentPrice
        return priceMovement * self.quantity

    def marketClose(self):
        quantity = self.market.positions[self.trader].quantity
        LongPosition(
            self.trader, self.market, quantity, "market", 
            self.leverage, reduceOnly=True
        )

    @staticmethod 
    def getPriceMovement(currentPosObject, entryPrice):
        return entryPrice - currentPosObject.entryPrice

    @classmethod
    def modifyPosition(
            cls, trader, market, quantity,
            entryPrice, leverage, reduceOnly
        ):

        cls.logTradeTimestamp(trader, market)

        currentPosition = market.positions[trader]
        if isinstance(currentPosition, LongPosition):
            currentPosition = cls.reducePosition(
                currentPosition, trader, market, quantity,
                entryPrice, leverage, reduceOnly 
            )

        elif isinstance(currentPosition, ShortPosition):
            currentPosition = cls.addPosition(
                currentPosition, trader, market, quantity,
                entryPrice, leverage, reduceOnly 
            )

        return currentPosition
