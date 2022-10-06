import datetime
import asyncio
from main import bot
from datetime import datetime
from pytzkt import TzKT
from main import connection, cursor


#async def get_ticket(sender):
#    try:
#        user_ticket = connection.execute(f"SELECT ticket FROM users WHERE adreses = {str(sender)}").fetchall()
#        ticket = [r[0] for r in user_ticket]
#    except:
#        ticket = 'None'
#    return ticket


tzkt = TzKT()


head = tzkt.get_head()

storage_adreses = []
last_transaction = []


async def infinity_wallet_updates():
    while True:
        try:
            user_adreses = connection.execute(
                f"SELECT ALL adreses FROM users").fetchall()
            for a in user_adreses:
                adreses = [r[0] for r in user_adreses]
                storage_adreses.append(adreses)
            for a in storage_adreses[0]:
                account = tzkt.get_account_operations(a)
                for a in account:
                    last_transaction.append(str(a['id']))
            await asyncio.sleep(120)
        except Exception as e:
            print(e)


async def infinity_transctions_updates():
    while True:
        try:
            for a in storage_adreses[0]:
                account = tzkt.get_account_operations(a)
                last_trans = account[0]['id']

                if str(last_trans) not in last_transaction:
                    times = account[0]['timestamp']
                    sender = account[0]['sender']['address']
                    target = account[0]['target']['address']
                    amount = account[0]['amount']
                    try:
                        alias_target = account[0]['target']['alias']
                    except:
                        alias_target = 'NoAlias'
                    try:
                        sender_alias = account[0]['sender']['alias']
                    except:
                        sender_alias = 'NoAlias'
                    try:
                        token_id = account[0]['parameter']['value'][0]['remove_operator']['token_id']
                    except:
                        token_id = 'NoToken'

                    if str(sender) in storage_adreses[0]:
                        user_ticket = connection.execute(
                            f"""SELECT ticket FROM users WHERE adreses = '{str(sender)}'""").fetchall()
                        ticket = [r[0] for r in user_ticket]
                        midq = connection.execute(
                            f"""SELECT id FROM users WHERE adreses = '{str(sender)}'""").fetchall()
                        mid = [r[0] for r in midq][0]
                        trgticket = 'NoTrgTicket'
                        if str(target) in storage_adreses[0]:
                            user_ticket = connection.execute(
                                f"""SELECT ticket FROM users WHERE adreses = '{str(target)}'""").fetchall()
                            trgticket = [r[0] for r in user_ticket]
                        message = f'⬆️OUT {str(amount)} TokenID: {str(token_id)} | {str(sender)} ({str(ticket)}) ({str(sender_alias)}) \n ➡️ {str(target)} ({str(alias_target)}) ({str(trgticket)} {str(times)}'
                        account = tzkt.get_account_operations(str(target))
                        today = datetime.today()
                        last_tr_day = account[-1]['timestamp'].replace('Z', '').replace('T', ' ')
                        last_tr_day = datetime.strptime(last_tr_day, '%Y-%m-%d %H:%M:%S')
                        a = last_tr_day - today
                        delta = str(a).split(' ')[0]
                        avgTxsForDay = int(len(account)) / int(delta)
                        if avgTxsForDay < 5:
                            if str(target) not in storage_adreses[0]:
                                cursor.execute(
                                    f"""INSERT INTO users (id, name, adreses, ticket) VALUES ('{str(mid)}', 'added bot', '{str(target)}', 'Bot Added')""")
                                connection.commit()
                        if avgTxsForDay > 5:
                            pass
                        account = tzkt.get_account_operations(str(sender))
                        for a in account:
                            last_transaction.append(str(a['id']))
                        await bot.send_message(mid, text=message)

                    if str(sender) not in storage_adreses[0]:
                        if str(target) in storage_adreses[0]:
                            midq = connection.execute(
                                f"""SELECT id FROM users WHERE adreses = '{str(target)}'""").fetchall()
                            mid = [r[0] for r in midq][0]
                            user_ticket = connection.execute(
                                f"""SELECT ticket FROM users WHERE adreses = '{str(target)}'""").fetchall()
                            ticket = [r[0] for r in user_ticket][0]
                            message = f'⬇️IN {str(amount)} TokenID: {str(token_id)} | {str(sender)} ({str(sender_alias)}) \n ➡️ {str(target)} ({str(alias_target)}) {str(ticket)} {str(times)}'
                            account = tzkt.get_account_operations(str(target))
                            for a in account:
                                last_transaction.append(str(a['id']))
                            await bot.send_message(mid, text=message)
            await asyncio.sleep(15)
        except Exception as e:
            print(e)
