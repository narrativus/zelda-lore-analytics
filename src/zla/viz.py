def timeline_bar(freq_series):
    import plotly.express as px
    fig = px.bar(freq_series, orientation="h",
                 labels={"value": "Mentions", "index": "Game"})
    fig.update_layout(title="Mentions of the Triforce over time")
    return fig
