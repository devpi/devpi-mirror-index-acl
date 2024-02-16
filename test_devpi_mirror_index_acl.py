from devpi_common.metadata import parse_version
from devpi_server import __version__ as _devpi_server_version
import pytest

devpi_server_version = parse_version(_devpi_server_version)
pytestmark = [pytest.mark.notransaction]

if devpi_server_version < parse_version("6.9.3dev"):
    from test_devpi_server.conftest import gentmp
    from test_devpi_server.conftest import httpget
    from test_devpi_server.conftest import makemapp
    from test_devpi_server.conftest import maketestapp
    from test_devpi_server.conftest import makexom
    from test_devpi_server.conftest import mapp
    from test_devpi_server.conftest import pypiurls
    from test_devpi_server.conftest import storage_info
    from test_devpi_server.conftest import testapp
    (
        gentmp,
        httpget,
        makemapp,
        maketestapp,
        makexom,
        mapp,
        pypiurls,
        storage_info,
        testapp,
    )
else:
    pytest_plugins = ["pytest_devpi_server", "test_devpi_server.plugin"]


@pytest.fixture
def xom(request, makexom):
    import devpi_mirror_index_acl
    xom = makexom(plugins=[
        (devpi_mirror_index_acl, None)])
    return xom


def test_mirror_index_acl(mapp, testapp, xom):
    app = testapp.app
    while 1:
        registry = getattr(app, "registry", None)
        if registry is not None:
            break
        app = app.app
    xom.config.args.acl_mirror_index_create = "root"
    mapp.create_and_login_user("user")
    mapp.create_index("user/mirror", code=403, indexconfig=dict(
        type="mirror"))
    xom.config.args.acl_mirror_index_create = None
    mapp.create_index("user/mirror", indexconfig=dict(
        type="mirror"))
