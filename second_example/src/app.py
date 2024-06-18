"""Example to show dashboard configuration."""
import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm

df = px.data.iris()

page = vm.Page(
    title="My first dashboard",
    components=[
        vm.Graph(figure=px.scatter(df, x="sepal_length", y="petal_width", color="species")),
        vm.Graph(figure=px.histogram(df, x="sepal_width", color="species")),            ],
    controls=[
        vm.Filter(column="species"),
    ],
)

dashboard = vm.Dashboard(pages=[page])

app = Vizro().build(dashboard)

######### GUNICORN #########
server = app.dash.server

######### FLASK #########
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5010, debug=True)  # nosec