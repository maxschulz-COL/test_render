"""Example to show dashboard configuration."""
from flask import request
from urllib import parse

import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro
from vizro.managers import data_manager


# Hack to stop app crashing when query parameters are specified: allow the layout function to accept **kwargs.
# Something like this will probably be built into vizro in the future so you wouldn't need to do this.
class DashboardWithQueryParameter(vm.Dashboard):
    def _make_page_layout(self, page: vm.Page, **kwargs):
        return super()._make_page_layout(page)


# Accessing query parameters as arguments to dynamic data loading functions should also be cleaner in future, but
# for now you can just access the flask request context to get the parameters.
# There's maybe some weird edge cases where this wouldn't work since it relies on HTTP referrer but I think it will
# be ok 99.999% of the time.
# The only real catch is that this is NOT compatible with caching. The cache key is just the dataset name "gapminder" and so
# wll not be differentiated dependent on the species. In future when we handle parameters properly this will work
# correctly.
def load_gapminder_query_country():
    default_species = "Germany"
    if request:
        query_parameters = parse.parse_qs(parse.urlparse(request.referrer).query)
        # If no country specified in query parameters then use default_species.
        # If multiple country specified like ?country=setosa&country=virginica, just take the first one.
        country = query_parameters.get("country", [default_species])[0]
    else:
        # No HTTP request - used during build phase of dashboard.
        country = default_species
    print(print(query_parameters))
    print(country)
    gapminder = px.data.gapminder()
    return gapminder[gapminder["country"] == country]


data_manager["gapminder"] = load_gapminder_query_country

page = vm.Page(
    title="Summary of the country in the gapminder dataset",
    components=[
        vm.Graph(figure=px.scatter("gapminder", x = "year",y = "pop",size = "lifeExp", color="gdpPercap", hover_name="country")),
    ],
)

dashboard = DashboardWithQueryParameter(pages=[page])

app = Vizro().build(dashboard)

######### GUNICORN #########
server = app.dash.server

######### FLASK #########
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)  # nosec