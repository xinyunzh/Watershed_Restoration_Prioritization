import pandas as pd
import numpy as np


def cal_watershed(df):
    """
    calculate the total nitrogen, total phosphorous, and total
    sediments of each watershed.

    :param df: pd.DataFrame
    :return watersheds: pd.DataFrame
    """

    # four "impervious" items
    imper = [1, 2, 3, 14]
    per = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16]

    # total pollution
    df['pollution'] = 0.
    for i in range(len(df)):
        if df.iloc[i, 1] in imper:
            df.set_value(i, 'pollution', df.iloc[i, 5] * (15.3 + 1.69 + 880))
        else:
            df.set_value(i, 'pollution', df.iloc[i, 5] * (10.8 + 0.43 + 140))

    # total nitrogen, total phosphorous, total sediments
    df['total_N'] = 0.
    df['total_P'] = 0.
    df['total_S'] = 0.
    for i in range(len(df)):
        if df.iloc[i, 1] in imper:
            df.set_value(i, 'total_N', df.iloc[i, 5] * 15.3)
            df.set_value(i, 'total_P', df.iloc[i, 5] * 1.69)
            df.set_value(i, 'total_S', df.iloc[i, 5] * 880)
        else:
            df.set_value(i, 'total_N', df.iloc[i, 5] * 10.8)
            df.set_value(i, 'total_P', df.iloc[i, 5] * 0.43)
            df.set_value(i, 'total_S', df.iloc[i, 5] * 140)

    # group by watersheds
    watersheds = df.groupby('DNR12DIG')['DNR12DIG', 'total_N', 'total_P', 'total_S'].sum()
    watersheds['watershed'] = watersheds.index
    watersheds.drop('DNR12DIG', 1, inplace = True)
    watersheds = watersheds[['watershed', 'total_N', 'total_P', 'total_S']]

    # convert 'watershed' column to String
    watersheds['watershed'] = watersheds['watershed'].astype('str')

    return watersheds


def main():
    # read data
    df = pd.read_excel('CB_LU_Ana.xlsx')
    watersheds = cal_watershed(df)

    # export .csv file
    watersheds.to_csv('CU-LU-Ana_claculated_watersheds.csv', index = False)


if __name__ == "__main__":
    main()
