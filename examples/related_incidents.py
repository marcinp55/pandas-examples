import pandas as pd
from datetime import datetime, timedelta


def calculate_related():
    working_days = pd.read_csv('./files/related_incidents/working_days.csv',
                               parse_dates=['date'])
    working_days = list(working_days['date'].dt.date)
    related_incidents_df = pd.read_csv('./files/related_incidents/related_incidents.csv',
                                       parse_dates=['impact_start', 'impact_end'])
    date_buckets = {}
    output_df = pd.DataFrame()

    for group_key, group_df in related_incidents_df.groupby(by=['end_user_id', 'fault']):
        group_df.apply(get_date_buckets,
                       args=(group_key, date_buckets, working_days),
                       axis=1)

    for group_key in date_buckets:
        for fault_period in date_buckets[group_key]:
            related_df = pd.DataFrame(date_buckets[group_key][fault_period])
            related_df['fault_period_start'] = fault_period[0]
            related_df['fault_period_end'] = fault_period[1]

            output_df = pd.concat([output_df, related_df])

    return output_df


def get_working_period(start_date: datetime.date, working_days: list):
    period_start_date = start_date
    working_days_index = None

    # Try to get the starting date of a working period
    while not working_days_index:
        try:
            working_days_index = working_days.index(period_start_date)
        # If period_start_date is not a working date, move one day
        # ahead in time, repeat until a working day is found
        except ValueError:
            period_start_date += timedelta(days=1)

    # Get all the working days in a working period,
    # 10 working days in this case
    period_end_date = working_days[working_days_index + 9]

    return start_date, period_end_date


def get_date_buckets(group_row: pd.Series, group_key: tuple, date_buckets: dict, working_days: list):
    # Check if there's already a (end_user_id, fault)
    # combination found, add empty dict if not
    if group_key not in date_buckets:
        date_buckets[group_key] = {}

    # If there are no working periods defined for (end_user_id, fault)
    # combination, create it and add current row
    if not date_buckets[group_key]:
        period_start_date, period_end_date = get_working_period(group_row['impact_end'].date(), working_days)
        date_buckets[group_key][(period_start_date, period_end_date)] = [group_row.copy()]
    else:
        working_period_found = False

        # If there already are any working periods in this bucket,
        # try to find a matching one for current row and
        # append if found
        for original_fault_period in date_buckets[group_key]:
            if original_fault_period[0] <= group_row['impact_start'].date() <= original_fault_period[1]:
                date_buckets[group_key][original_fault_period].append(group_row.copy())
                working_period_found = True
                break

        # If the (end_user_id, fault) combination doesn't fit
        # into any of existing working periods, add a new one
        if not working_period_found:
            period_start_date, period_end_date = get_working_period(group_row['impact_end'].date(), working_days)
            date_buckets[group_key][(period_start_date, period_end_date)] = [group_row.copy()]

    return group_row


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)

    final_df = calculate_related()
    print(final_df)
