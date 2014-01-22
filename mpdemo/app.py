import morepath
import waitress


# the morepath application that contains configuration and is
# WSGI app
app = morepath.App()


# the root path for the application
@app.path(path='')
class Root(object):
    pass


# individual model with id under root
class Model(object):
    def __init__(self, id):
        self.id = id


# publish model under root under {id}
@app.path(model=Model, path="{id}",
          variables=lambda model: {'id': model.id})
def get_model(id):
    return Model(id)


# the default view for the root is a list of links
# to models
@app.view(model=Root, render=morepath.render_html)
def root_default(request, model):
    result = []
    for i in range(10):
        result.append(
            '<p><a href="%s">Link to %s</a></p>' % (request.link(Model(i)),
                                                    i))
    return ''.join(result)


# the default view for a model
@app.view(model=Model, render=morepath.render_html)
def model_default(request, model):
    return '<p>I am the model: %s</p>' % model.id


def main():
    # set up morepath's own configuration
    config = morepath.setup()
    # load application specific configuration
    config.scan()
    config.commit()

    # serve app as WSGI app
    waitress.serve(app)
