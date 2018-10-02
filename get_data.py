import json 
import requests 
import sys
import time


if(len(sys.argv) != 2): 
    print("Get Data from coinmarketcap")
    print("Use: python3 get_data.py coin_list.lis")
    quit()


try:
    file_data = open(sys.argv[1],"r")    
except FileNotFoundError:
    print("The file \"%s\" is missing" % sys.argv[1])
    quit()
    


#It gets the list of coins

my_list_of_coins = []

for row in file_data:         
    my_list_of_coins.append(row.strip())

file_data.close()


#Printing my coins
print("My coins:")
for i in range(len(my_list_of_coins)):
    print(i+1, "-", my_list_of_coins[i])

    
    

line_requests = 'https://api.coinmarketcap.com/v1/ticker/'

BTC_price = 1.0

while True:
    
    for one_name in my_list_of_coins:
    
        line = line_requests + one_name
    
        try:
            r = requests.get(line)
        except requests.exceptions.RequestException:
            print("Error of connection!!!")
            break
        
        try:
            r.json()
        except ValueError:
            print("Error of format JSON")
            break
        
        for coin in r.json():
            if(one_name == 'bitcoin'): BTC_price = float(coin['price_usd'])
        
            file_out_name = coin['symbol'] + '.dat'
            file_out = open(file_out_name, "a") 
        
        
            file_out.write(str(float(coin['last_updated'])/3600.0) + ' ' + coin['price_usd'] + ' ' + coin['price_btc'] + ' ' + coin['24h_volume_usd'] + ' ' + str(float(coin['24h_volume_usd'])/BTC_price) + ' ' + str(time.ctime(int(coin['last_updated']))) + '\n')
        
            file_out.close();

    time.sleep(300)
