from flask.ext.appbuilder import IndexView


class LandingView(IndexView):
    index_template = 'index.html'