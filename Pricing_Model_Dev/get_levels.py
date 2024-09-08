from Datasets import get_data

df = get_data()


print(df.VehPower.unique())
print(df.VehAge.unique())
print(df.DrivAge.unique())
print(df.BonusMalus.unique())
print(df.VehGas.unique())
print(df.Area.unique())