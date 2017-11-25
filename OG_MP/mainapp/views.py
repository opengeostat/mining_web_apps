from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
import json
import quandl
from . import forms
from django.http import HttpResponse, JsonResponse, Http404
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool, Range1d

quandl.ApiConfig.api_key = 'hEK_VDFz71bd88AKikmB'


def index(request):
    form = forms.MineralForm(initial={'end_year': '2017'})
    return render(request, 'mainapp/index.html', {"form": form})


def data_visualizer(request):
    form = forms.MineralForm(request.GET)
    if form.is_valid():
        start_year = form.cleaned_data['start_year']
        end_year = form.cleaned_data['end_year']
        mineral = form.cleaned_data['mineral']
        values = quandl.get("LME/PR_{mineral}".format(mineral=mineral), start_date="{year}-01-01".format(year=start_year), end_date="{year}-12-31".format(year=end_year))
        avg = values["Cash Buyer"].mean()
        values["mean"] = avg
        m = values["mean"].values
        x = values["Cash Buyer"].keys()
        y = values["Cash Buyer"].values
        plot = figure(title="Stock Price for {mineral} {start}/01/01-{end}/12/31".format(mineral=mineral, start=start_year, end=end_year),
                      x_axis_label='date',
                      y_axis_label='price',
                      plot_width =800,
                      plot_height =400,
                      responsive=True,
                      x_axis_type="datetime",
                      toolbar_location="right",
                     )
        plot.y_range = Range1d(1500, 3000)
        price_line = plot.line(x, y, color='#ff8c43', line_width=1, line_alpha=0.5, legend='price')
        hover = HoverTool(tooltips=[
            ("date", "@x{%F}"),
            ("price", "@y")
        ],
        renderers=[price_line],  # show tooltip for only one line
        formatters={
            'x'      : 'datetime', # use 'datetime' formatter for 'date' field
            'y' : 'printf',   # use 'printf' formatter for 'adj close' field
        },
        mode='vline')
        hover.formatters = {"x": "datetime"}  # trasnform value of x to date
        plot.line(x, m, color='black',line_width=2, line_alpha=0.2, legend='mean', line_dash="4 4")  # mean line
        plot.add_tools(hover)
        script, graph = components(plot, CDN)
        return render(request, 'mainapp/index.html', {"form": form, "script": script, "graph": graph, "avg": avg})
    else:
        return render(request, 'mainapp/index.html', {"form": form})
