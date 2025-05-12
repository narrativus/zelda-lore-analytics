def frequency_by_game(df, motif):
    return df.query("theme == @motif").groupby("game")["count"].sum().sort_values()
