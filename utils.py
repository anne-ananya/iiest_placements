def filter_by_department(df, department):
    if department != 'All':
        return df[df['Department'] == department]
    return df
