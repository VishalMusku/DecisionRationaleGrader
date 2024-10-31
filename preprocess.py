import pandas as pd



def process_excel(file_path):

    sheet_df = pd.read_excel(file_path, sheet_name="Rationale")  # Load only the specified sheet

    # Filter for rows where 'Week' is 4 and 'Industry' is not 'benchmark'
    week_4_df = sheet_df[(sheet_df['Week'] == 4) & (sheet_df['Industry'] != 'benchmark')]

    # Sort by 'Message Date' to ensure messages are ordered before grouping
    week_4_df = week_4_df.sort_values(by=['Industry', 'Firm', 'Week', 'Message Date'])

    # Group by 'Industry', 'Firm', and 'Week' and aggregate as specified for Week 4
    week_4_result = week_4_df.groupby(['Industry', 'Firm', 'Week'], as_index=False).agg({
        'Message Date': 'first',         # Keep the earliest date
        'Name': 'first',                 # Keep the Name associated with the earliest date
        'Message': ' '.join               # Concatenate messages in the sorted order
    })

    # Get a list of firms from Week 3 for which we need to create empty messages in Week 4
    week_3_df = sheet_df[(sheet_df['Week'] == 3) & (sheet_df['Industry'] != 'benchmark')]

    # Extract unique firms and names from Week 3
    week_3_firms = week_3_df[['Industry', 'Firm', 'Name']].drop_duplicates()

    # Identify firms that did not submit messages in Week 4
    firms_with_no_week_4_submission = week_3_firms[~week_3_firms[['Industry', 'Firm']].apply(tuple, 1).isin(week_4_result[['Industry', 'Firm']].apply(tuple, 1))]

    # Select a single name for each firm without a submission in Week 4
    # Use the first name found in Week 3 for simplicity
    empty_message_rows = (
        firms_with_no_week_4_submission
        .groupby(['Industry', 'Firm'])
        .agg({'Name': 'first'})  # Take the first name for each firm
        .reset_index()
    )

    # Create new rows for these firms with empty messages for Week 4
    empty_message_rows['Week'] = 4
    empty_message_rows['Message Date'] = ''  # Keep message date empty
    empty_message_rows['Message'] = ''        # Keep message empty

    # Combine the Week 4 results with the empty message rows
    final_result = pd.concat([week_4_result, empty_message_rows], ignore_index=True)

    # Sort the final DataFrame
    final_result = final_result.sort_values(by=['Industry', 'Firm', 'Week'])


    # Optionally, save the result to a new Excel file
    final_result.to_excel("/Users/vishalreddy/Desktop/Rationale_grading 2/data.xlsx", index=False)

    return final_result



