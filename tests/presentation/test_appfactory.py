from puppeter.presentation.appfactory import AppFactory


def test_app_factory_interactive():
    # given
    factory = AppFactory()
    # when
    app = factory.interactive({'answers': None})
    runmethod = app.run
    # then
    assert app is not None
    assert callable(runmethod)


def test_app_factory_unattended():
    # given
    factory = AppFactory()
    # when
    app = factory.unattended({'answers': __file__})
    runmethod = app.run
    # then
    assert app is not None
    assert callable(runmethod)
