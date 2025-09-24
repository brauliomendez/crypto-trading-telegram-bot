import exchange
import env_secrets
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("Hi! 🚀")

async def help(update, _):
    await update.message.reply_text(f"Available commands:\n/price\n/buy\n/sell")

async def price(update, _):
    price = ex.fetch_ticker(SYMBOL)
    await update.message.reply_text(f"{SYMBOL} ahora: {price}$")


SIMULATED = True
ex = exchange.Exchange(simulated=SIMULATED)
SYMBOL = "ETH/USDC"

amount=0
quote_amount=50 #$
in_position=False

async def buy(update, _):
    global amount
    global quote_amount
    global in_position

    if not in_position:
        try:
            if SIMULATED:
                price = ex.fetch_ticker(SYMBOL)

            buy_order = ex.buy(SYMBOL, quote_amount, simulated_price=price)
            amount = buy_order['purchased_amount']
            price = buy_order['price']
            total_cost = buy_order['total_cost']
            in_position = True
            await update.message.reply_text(f"BUY: {amount} {SYMBOL} @ {price}$ ({total_cost}$)")
        except Exception as e:
            await update.message.reply_text(f"Error:\n{e}")
    else:
        await update.message.reply_text(f"Already in position")

async def sell(update, _):
    global amount
    global in_position

    if in_position:
        try:
            if SIMULATED:
                price = ex.fetch_ticker(SYMBOL)
            
            sell_order = ex.sell(SYMBOL, amount, simulated_price=price)
            price = sell_order['price']
            total_recovered = sell_order['total_recovered']
            in_position = False
            await update.message.reply_text(f"SELL: {amount} {SYMBOL} @ {price}$ ({total_recovered}$)")
        except Exception as e:
            await update.message.reply_text(f"Error:\n{e}")
    else:
        await update.message.reply_text(f"Not in position")

def main():
    app = Application.builder().token(env_secrets.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("sell", sell))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help))
    app.run_polling()

if __name__ == "__main__":
    main()