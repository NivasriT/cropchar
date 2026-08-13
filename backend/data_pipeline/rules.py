def is_unauthorized(field_id, acq_date, permits_df):
    row = permits_df[permits_df.field_id == field_id]

    if row.empty:
        return True  # no permit on file = unauthorized by default

    row = row.iloc[0]

    in_season = row.season_start <= acq_date <= row.season_end

    return in_season and not row.permitted