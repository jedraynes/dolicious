#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 22:11:42 2020

@author: jedraynes

Shoutout to the amazing people at StackOverflow :)

https://github.com/jedraynes/dolicious

If you plan to visualize the resulting csv yourself, consider unpivoting the data.
"""
def main():
    import requests
    from bs4 import BeautifulSoup
    import pandas as pd
    import sys
    
    # scraping the website
    print('Setting up the scraper and scraping the website using bs4...')
    url = 'https://www.dol.gov/agencies/whd/state/minimum-wage/history'
    page = requests.get(url)
    plain_text = page.text
    soup = BeautifulSoup(plain_text, 'lxml')
    rows = soup.findAll('tr')
    locations = []
    print('...done!')
    
    # building the matrix of data
    print('Creating the first dataframe from the scraped results...')
    for row in range(len(rows)):
        location_row = []
        # column headers are in 'th' and column values are in 'td'
        columns = rows[row].find_all(['th', 'td'])
        for column in columns:
            location_row.append(column.getText())
        locations.append(location_row)
    
    # creating the dirty dataframe from out list    
    df_dirty = pd.DataFrame(locations)
    print('...done!')
    
    # individual data sets as displayed on DOL website
    print('Parsing the data into multiple tables...')
    df_1968_1981 = df_dirty.iloc[0:56]
    df_1988_1998 = df_dirty.iloc[56:112]
    df_2000_2006 = df_dirty.iloc[112:168]
    df_2007_2013 = df_dirty.iloc[168:224]
    df_2014_2019 = df_dirty.iloc[224:280]
    print('...done!')
    
    # merging the individual tables into one table
    print('Merging the individual tables...')
    df_1968_1998 = pd.merge(df_1968_1981, df_1988_1998, on = 0)
    df_1968_2006 = pd.merge(df_1968_1998, df_2000_2006, on = 0)
    df_1968_2013 = pd.merge(df_1968_2006, df_2007_2013, on = 0)
    df_cleaner = pd.merge(df_1968_2013, df_2014_2019, on = 0)
    print('...done!')
    
    # promote headers
    print('Promoting headers...')
    periods = df_cleaner.iloc[0]
    df_cleaner = df_cleaner[1:]
    df_cleaner.columns = periods
    print('...done!')
    
    # extract lowest value in cell, conservatism
    print('Extracting the lowest float for conservatism...')
    df_cleaner_v2 = df_cleaner
    for column in df_cleaner.columns[1:]:
        # takes the first float that is seen in the cell
        # this is needed as sometimes there are two values, the lowest is taken
        df_cleaner_v2[column] = df_cleaner[column].str.extract(r'(\d+.\d+)').astype('float')
    print('...done!')
    
    # replace NaN values with federal minimum
    print('Replacing NaN values with the federal minium...')
    df_cleaner_v3 = df_cleaner_v2
    for column in df_cleaner_v2.columns[1:]:
        df_cleaner_v3[column] = df_cleaner_v2[column].fillna(df_cleaner_v2.loc[1, column])
    print('...done!')
    
    # drop last column as it's NaN
    print('Dropping  any columns with NaNs...')
    df_cleaner_v4 = df_cleaner_v3.dropna(axis = 1)
    print('...done!')
    
    # rename headers
    print('Renaming headers...')
    df_cleaner_v5 = df_cleaner_v4.rename(columns = {'State or other\n\t\t\tjurisdiction': 'location', '1968 (a)': '1968', '1970 (a)': '1970', '1972 (a)': '1972', '1976 (a)': '1976'})
    print('...done!')
    
    # set the locaion as the index
    print('Setting location as the index...')
    df = df_cleaner_v5.set_index('location', drop = False)
    print('...done!')
        
    # save as csv
    print('Saving as csv...')
    confirm = input('Save the file as a csv? y/n: ')
    path = '/Users/jedraynes/Documents/Python/Dolicious/'
    if confirm == 'y':
        df.to_csv(path+'dol_min_wage_scraped.csv', index = False)
        print('...done!')
    else:
        print('Script canceled. Exiting...')
        sys.exit()
    return

if __name__ == '__main__':
    main()
