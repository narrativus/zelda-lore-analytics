def timeline_bar(freq_series):
    import plotly.express as px

    fig = px.bar(
        freq_series, orientation="h", labels={"value": "Mentions", "index": "Game"}
    )
    fig.update_layout(title="Mentions of the Triforce over time")
    return fig


def network(df, motif):
    """Very simple placeholder network graph so the app runs."""
    import plotly.graph_objs as go

    # Empty figure – replace with real network later
    return go.Figure(go.Scatter(x=[], y=[]))
