from os import read
import pandas as pd
import datetime
import os

from pandas.core.arrays import boolean

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_code(self):
        return self.item_code

    def get_name(self):
        return self.item_name

    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_name_list = []
        self.item_price_list = []
        self.item_quantity = []
        self.item_master=item_master
   
    def add_item_order(self,item_code, item_name,item_price,item_quantity):
        self.item_order_list.append(item_code)
        self.item_name_list.append(item_name)
        self.item_price_list.append(item_price)
        self.item_quantity.append(item_quantity)
        
    def view_item_list(self):
        for i in range(len(self.item_order_list)):
            sum = int(self.item_quantity[i]) * int(self.item_price_list[i])
            print("商品コード:{}".format(self.item_order_list[i]),"商品名:{}".format(self.item_name_list[i]),"値段:{}".format(self.item_price_list[i]), "個数:{}".format(self.item_quantity[i]), "合計金額:{}".format(sum))

    def make_item_list_recept(self, file_name):
        text = '------注文品-----'
        self.make_order_recept(text,file_name)
        text = ''
        for i in range(len(self.item_order_list)):
            sum = int(self.item_quantity[i]) * int(self.item_price_list[i])
            tuple = "商品コード:{}".format(self.item_order_list[i]),"商品名:{}".format(self.item_name_list[i]),"値段:{}".format(self.item_price_list[i]), "個数:{}".format(self.item_quantity[i]), "合計金額:{}".format(sum)
            for string in tuple:
                text += string + ","
            self.make_order_recept(text, file_name)
            text = ''

    #不要コード
    def registration(self, item_code):
        #アイテム登録
        name = input("名前を入力してください>>> ")
        #price = int(input("値段を入力してください>>> "))
        #個数の追加     
        quantity = input('個数を入力してください')

        if len(item_code) == 1:
            item_code = "00" + item_code
        elif len(item_code) == 2:
            item_code = "0" + item_code
        else:
            item_code = item_code
        self.add_item_order(item_code, name)
    
    def get_sum_price(self):
        sum = 0
        for price, quantity in zip(self.item_price_list, self.item_quantity):
            sum += int(price) * int(quantity)
        return sum
    
    def make_recept_sumprice(self, file_name):
        text = '-----合計金額-----'
        self.make_order_recept(text, file_name)
        sum = 0
        for price, quantity in zip(self.item_price_list, self.item_quantity):
            sum += int(price) * int(quantity)
        text = sum
        self.make_order_recept(text, file_name)
    
    def make_order_recept(self,text, file_name):
        path = './recept/' + file_name
        text = str(text)

        if os.path.exists(path):
            with open(path, mode = 'a') as f:
                f.write('\n' + text)
        else:
            with open(path, mode = 'w') as f:
                f.write(text)

class Allowwance:
    def __init__(self,price) -> None:
        self.price = price
    
    def calcurate(self, money) -> boolean:
        back = money - self.price
        if back < 0:
            print("支払い金額が{}円足りません".format(0-back))
            return False
        else:
            print("支払いが完了しました")
            print("お釣りは{}円です".format(back))
            return True
    
    def make_recept_calcurate(self, money, file_name):
        text = '-----お支払い金額-----'
        self.make_recept(text, file_name)
        text = money
        self.make_recept(text, file_name)
        back = money - self.price
        text = '-----お釣り-----'
        self.make_recept(text, file_name)
        text = "お釣りは{}円です".format(back)
        self.make_recept(text, file_name)

    def make_recept(self, text,file_name):
        path = './recept/' + file_name
        text = str(text)
        with open(path, mode = 'a') as f:
            f.write('\n' + text)

### メイン処理
def main():
    dt_now = datetime.datetime.now()
    file_name = str(dt_now.year) + '-' + str(dt_now.month) + '-' + str(dt_now.day) + '-' + str(dt_now.hour) + '-' + str(dt_now.minute) + '-' + str(dt_now.second)
    #csv読み込み
    df = pd.read_csv('./master.csv', header = None, dtype=object)
    read_csv = []
    for i in range(len(df)):
        read_csv.append(df.iloc[i].tolist())
    # マスタ登録
    item_master = []

    for item in read_csv:
        item_master.append(Item(item[0], item[1], int(item[2])))

    print("-------売り物リスト---------")
    for item in item_master:
        print("name:{}".format(item.get_name()), "price:{}".format(item.get_price()))
    print("--------------------------")
    # オーダー登録
    item_order = Order(item_master)
    pre_item_code = item_master[-1].get_code()
    now_item_code = str(int(pre_item_code) + 1)
    
    #order.registration(now_item_code)
    while True:
        flag = 0
        name = input("名前を入力してください>>> ") 

        for item in item_master:
            if item.get_name() == name:
                item_code = item.get_code()
                item_price = item.get_price()
                flag = 1
            else:
                pass

        if flag == 1:
            quantity = input('個数を入力してください>>> ')
            item_order.add_item_order(item_code, name, item_price, quantity)
        else:
            print("そんな商品はありません！！")

        if input("買い物を続けますか?[y/n] >>> ") == 'y':
            pass
        else:
            break

        # オーダー表示
    print("-------注文品---------")
    item_order.view_item_list()

    print("-------合計金額--------")
    sum = item_order.get_sum_price()
    print("合計金額:{}".format(sum))
    
    item_allowwance = Allowwance(sum)

    print("---------勘定---------")
    money = input("お金ください>>> ")
    money = int(money)
    result = item_allowwance.calcurate(money)
    print("---------------------")

    #recept作成
    if result is True:
        item_order.make_item_list_recept(file_name)
        item_order.make_recept_sumprice(file_name)
        item_allowwance.make_recept_calcurate(money, file_name)

if __name__ == "__main__":
    main()