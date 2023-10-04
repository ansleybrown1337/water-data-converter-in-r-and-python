'''
Water Quality Data Format Converter
-----------------------------------
Author: A.J. Brown
Position: Agricultural Data Scientist
Email: Ansley.Brown@colostate.edu

Description:
This script provides functionalities to convert between new and old water 
quality data formats. It's designed as both a utility tool and an educational 
resource to showcase data conversion methodologies in Python.
'''

# Import packages
import pandas as pd

# Import data
df_old = pd.read_csv('data/old_data_format.csv')
df_new = pd.read_csv('data/new_data_format.csv')

# Create dictonary to map equivalent columns and analyte names between formats
format_dictionary = {
    'op': 'Phosphorus, Total Orthophosphate (as P)',
    'no2': 'Nitrogen, Nitrite  (As N)',
    'no3': 'Nitrogen, Nitrate (As N)',
    'tkn': 'Nitrogen, Total Kjeldahl',
    'tp': 'Phosphorus, Total (As P)',
    'selenium (mg/L)': 'Selenium, Total',
    'tss': 'TSS',
    'Location': 'location.name',
    'Date': 'date',
    'Irr/Storm': 'event.count',
    'Station': 'treatment.name',
    'Dup': 'duplicate',
    'ID': 'sample.id'
    # the remaining columns have no overlap between formats
}

# Define functions
def convert_old_to_new(old_df, format_dict, output_csv = False):
    '''
    Converts old data format to new data format.
    inputs:
        old_df: pandas dataframe of old data format
        format_dict: dictionary of new/old column names and analyte names
    '''
    # Pivot the data based on the 'analyte' column using the new format_dict
    pivoted_data = (
        new_data.pivot_table(
            index=[format_dict['ID'], format_dict['Location'], 
                   format_dict['Date'], 'event.type', format_dict['Station'],
                   'event'],
            columns='analyte',
            values='result',
            aggfunc='first'
        )
        .reset_index()
    )

    # Rename columns based on format_dict for consistency
    pivoted_data.rename(
        columns={value: key for key, value in format_dict.items()},
        inplace=True)

    # Merging back to get non-analyte columns
    merged_data = pd.merge(
        new_data.drop_duplicates(subset=[format_dict['ID']]),
        pivoted_data,
        on=[format_dict['ID'], format_dict['Location'], format_dict['Date'], 
            'event.type', format_dict['Station'], 'event'],
        how='left'
    )

    # Output the data as a csv if desired
    if output_csv == False:
        pd.DataFrame.to_csv(merged_data, 'Output/converted_old_to_new_data.csv')
        
    # Return the data for further processing if desired        
    return merged_data