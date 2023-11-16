# %% [markdown]
# # Testing Panel with hello world
# 
# ## Source
# 
# * https://panel.holoviz.org/getting_started/build_app.html

# %%
# first print Python version
import sys
print(f"Python version: {sys.version}")

# %%
import panel as pn
import hvplot as hv
import hvplot.pandas
import pandas as pd
import numpy as np

# print panel version
print(f"Panel version: {pn.__version__}")

# print hvplot version
print(f"HVPlot version: {hv.__version__}")

# print pandas version
print(f"Pandas version: {pd.__version__}")

# print numpy version
print(f"Numpy version: {np.__version__}")


# %%
# pn.extension(design='material')
pn.extension(comms='vscode')

csv_file = ("https://raw.githubusercontent.com/holoviz/panel/main/examples/assets/occupancy.csv")
data = pd.read_csv(csv_file, parse_dates=["date"], index_col="date")

data.tail()

# %%
def transform_data(variable, window, sigma):
    ''' Calculates the rolling average and the outliers '''
    avg = data[variable].rolling(window=window).mean()
    residual = data[variable] - avg
    std = residual.rolling(window=window).std()
    outliers = np.abs(residual) > std * sigma
    return avg, avg[outliers]

def create_plot(variable="Temperature", window=30, sigma=10):
    ''' Plots the rolling average and the outliers '''
    avg, highlight = transform_data(variable, window, sigma)
    return avg.hvplot(height=300, width=400, legend=False) * highlight.hvplot.scatter(
        color="orange", padding=0.1, legend=False
    )

# %%
create_plot(variable='Temperature', window=20, sigma=10)

# %%
variable_widget = pn.widgets.Select(name="variable", value="Temperature", options=list(data.columns))
window_widget = pn.widgets.IntSlider(name="window", value=30, start=1, end=60)
sigma_widget = pn.widgets.IntSlider(name="sigma", value=10, start=0, end=20)

# %% [markdown]
# ## Binding widgets with pn.bind
# 
# Now that we have a function and some widgets, let’s link them together so that updates to the widgets rerun the function. One easy way to create this link in Panel is with pn.bind:

# %%
bound_plot = pn.bind(create_plot, variable=variable_widget, window=window_widget, sigma=sigma_widget)

# %%
first_app = pn.Column(variable_widget, window_widget, sigma_widget, bound_plot)
# change app size
## FIXME [Open Browser Console for more detailed log - Double click to close this message]
# Failed to load model class 'BokehModel' from module '@bokeh/jupyter_bokeh'
# Error: No version of module @bokeh/jupyter_bokeh is registered

first_app.servable()


