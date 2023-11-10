import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def line_plotter(df, date_col, quarter_type, category, value, 
                 legend, ylabel, title, figsize=(12,6), line_width=3):
    """
    This function takes a dataframe for plotting a line graph over
    time series using the date column with a quarter type (year or month)
    and grouping the values for each category in the quarter type
    """
    # To declare a date time column for time series plotting.
    df[date_col] = pd.to_datetime(df[date_col])

    # Separate the years into a different column to pivot.
    df['Year'] = df[date_col].dt.year
    df['Month'] = df[date_col].dt.month

    # To group value of each category instance over the quarter_type 
    # and pivot them into a single table.
    df_grouped = df.groupby([quarter_type, category])\
                            [value].sum().reset_index()
    df_pivot = df_grouped.pivot(index=quarter_type, 
                                columns=category, values=value)

    # Creating a line plot for visualization.
    df_pivot.plot(kind='line', figsize=figsize, lw=line_width)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend(title=legend)
    plt.show()



def stack_plotter(df, category, value, group, title, \
                  legend, xlabel, ylabel, figsize=(12, 6)):
    """
    This function returns a stacked bar plot of 'Value'
    by 'Category' and 'Group' specified by the user in
    Dataframe 'df' and set the title and axis labels.
    default figure size is (12, 6) by can be specified
    as per the requirement.
    """

    # Grouping values by Category and Group and Summing the target column.
    df_grouped = df.groupby([category, group] \
                                     )[value].sum().reset_index()

    #Creating a pivot of the table to use in stack efficiently.
    df_pivoted = df_grouped.pivot(index=category, columns=group, values=value)

    df_pivoted.plot(kind='bar', stacked=True, figsize=figsize)
    
    # Plot settings    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend(title=legend)
    plt.grid(True)
    plt.show()


def pie_plotter(df, category, value, title):
    """
    This function creates a pie plot of the provided 'Category'
    of the Dataframe (df) against the target variable as 'Value'.
    """

    # Applying filter by category.
    filtered_df = df.groupby(category).sum().reset_index()

    plt.figure(figsize=(12,6))

    plt.pie(filtered_df[value], autopct="%1.1f%%", 
            labels=filtered_df[category])
    plt.title(title)
    plt.show()


# Acquiring a dataframe of the dataset including our variables.
mi_df = pd.read_csv('./Data/MentalIllness_data.csv')

# Lets separate the data for rows marked as True for Mental Illness diagnosis.
diagnosed = mi_df[mi_df['Mental Illness (Diagnosed)']==True]

# Converting Target column to integer to aid aggregation functions
diagnosed['Mental Illness (Diagnosed)'] = \
            diagnosed['Mental Illness (Diagnosed)'].astype(int)

# Importing a dataset feasible for line plots.
tech_stocks = pd.read_csv('./Data/Tech_stocks.csv')

# Plotting a line chart to differentiate between stock trade volumes of
# Major tech companies
line_plotter(tech_stocks,'Date', 'Year',
                'Company',
                'Volume', 'Company',
                'Volume in e^10', 'Stock Trade Volume by year',
                line_width=3)

# Plotting a stacked bar chart for mental illness between tech company
# Employees in different age groups with ob types as stacks.  
stack_plotter(diagnosed, 'Age Group', 'Mental Illness (Diagnosed)', 
                'Job Type',
                'Cases Diagnosed/Age Group with Job Type', 
                'Job Type',
                'Age Groups',
                'Number of Cases',)

# Plotting a pie chart to distinguish the afore-mentioned 
# mental illness cases Gender-wise.
pie_plotter(diagnosed, 'Gender', 'Mental Illness (Diagnosed)', 
            'Mental Illness Cases by Gender')

