import pandas as pd
import random


data = pd.read_csv('../wld_trs_ports_wfp.csv', usecols=['country', 'portname'])
data.dropna(inplace=True)
for i in range(data.shape[0]):
    price = random.randint(100, 5000)
    levelid = random.randint(1, 4)

    command = "INSERT INTO tb_Ports(IDPort, Country, NamePort, Price, LevelID) VALUES(" + str(i + 1) + ", '" + data.iloc[i, 0] + "', '" + data.iloc[i, 1] + "', " + str(price) + ", " + str(levelid) + ");"

    print(command)
