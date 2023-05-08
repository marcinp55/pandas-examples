import pandas as pd


def basic_example():
    output_df = pd.DataFrame({
        'A': ['Old_A1', 'Old_A2'],
        'B': ['Old_B1', 'Old_B2']
    })

    update_df = pd.DataFrame({
        'A': ['New_A1', 'New_A2']
    })

    output_df.update(update_df)
    print(output_df)


def not_aligning_example():
    output_df = pd.DataFrame({
        'A': ['Old_A1', 'Old_A2'],
        'B': ['Old_B1', 'Old_B2']
    })

    update_col_df = pd.DataFrame({
        'C': ['New_A1', 'New_A2']
    })

    update_index_df = pd.DataFrame({
        'A': ['New_A1', 'New_A2']
    }, index=[2, 3])

    output_df.update(update_col_df)
    output_df.update(update_index_df)
    print(output_df)


def manual_overrides():
    source_df = pd.DataFrame({
        'issue_key': ['T-1', 'T-2', 'T-3'],
        'start_ts': [
            pd.Timestamp('2023-05-08 10:15:00'),
            pd.Timestamp('2023-05-09 09:30:00'),
            pd.Timestamp('2023-05-10 13:00:00')
        ],
        'resolve_ts': [
            pd.Timestamp('2023-05-08 11:30:00'),
            pd.Timestamp('2023-05-10 11:15:00'),
            pd.Timestamp('2023-05-12 15:00:00')
        ]
    })

    manual_overrides_df = pd.DataFrame({
        'key': ['T-2', 'T-3'],
        'resolve_ts': [
            pd.Timestamp('2023-05-09 15:10:00'),
            pd.Timestamp('2023-05-10 14:00:00')
        ]
    })

    source_df.set_index('issue_key', inplace=True)
    manual_overrides_df.set_index('key', inplace=True)
    source_df.update(manual_overrides_df)
    source_df.reset_index(inplace=True)

    print(source_df)


def updating_with_defaults():
    output_df = pd.DataFrame({
        'A': ['A1', 'A2', 'A3'],
        'B': ['B1', None, 'B3'],
        'C': [None, None, 'C3']
    })

    manual_overrides_df = pd.DataFrame({
        'A': ['Default_A'],
        'B': ['Default_B'],
        'C': ['Default_C']
    })

    output_df.set_index(pd.Index([0] * len(output_df)), inplace=True)
    manual_overrides_df.set_index(pd.Index([0] * len(manual_overrides_df)), inplace=True)

    output_df.update(manual_overrides_df, overwrite=False)
    output_df.reset_index(drop=True, inplace=True)

    print(output_df)


def update_with_null_values():
    output_df = pd.DataFrame({
        'key': ['M-1', 'M-2', 'M-3'],
        'A': ['A1', 'A2', 'A3'],
        'B': ['B1', 'B2', 'B3'],
        'C': ['C1', 'C2', 'C3']
    }).set_index('key')

    manual_overrides_df = pd.DataFrame({
        'key': ['M-2', 'M-3'],
        'A': ['New_A2', None],
        'B': [None, 'New_B3'],
        'C': [None, None]
    }).set_index('key')

    output_df.update(manual_overrides_df)
    output_df.reset_index(inplace=True)

    print(output_df)


def using_multi_index():
    output_df = pd.DataFrame({
        'address_id': [1, 2, 2],
        'user_id': [4, 5, 6],
        'A': ['A1', 'A2', 'A3'],
        'B': ['B1', 'B2', 'B3']
    }).set_index(['address_id', 'user_id'])

    update_df = pd.DataFrame({
        'address_id': [1, 2],
        'user_id': [4, 6],
        'A': ['New_A1', 'New_A3'],
        'B': ['New_B1', 'New_B3']
    }).set_index(['address_id', 'user_id'])

    output_df.update(update_df)
    output_df.reset_index(inplace=True)

    print(output_df)


def using_update_filter_function():
    output_df = pd.DataFrame({
        'key': ['K-1', 'K-2'],
        'A': ['DoNotUpdate', 'A2'],
        'B': ['B1', 'B2'],
        'C': ['DoNotUpdate', 'C2']
    }).set_index('key')

    manual_overrides_df = pd.DataFrame({
        'key': ['K-1'],
        'A': ['New_A1'],
        'B': ['New_B1'],
        'C': ['New_C1']
    }).set_index('key')

    output_df.update(manual_overrides_df, filter_func=lambda df_value: df_value != 'DoNotUpdate')
    output_df.reset_index(inplace=True)

    print(output_df)
