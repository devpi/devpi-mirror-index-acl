import pytest


pytestmark = [pytest.mark.notransaction]
pytest_plugins = ["pytest_devpi_server", "test_devpi_server.plugin"]


@pytest.fixture
def remote_index_info(server_version):
    from devpi_common.metadata import parse_version

    if server_version < parse_version("7.0.0.dev2"):

        class MirrorInfo:
            type = "mirror"

        return MirrorInfo()

    class RemoteInfo:
        type = "remote"

    return RemoteInfo()


@pytest.fixture
def xom(request, makexom):
    import devpi_mirror_index_acl
    xom = makexom(plugins=[
        (devpi_mirror_index_acl, None)])
    return xom


def test_mirror_index_acl(mapp, remote_index_info, testapp, xom):
    xom.config.args.acl_mirror_index_create = "root"
    mapp.login_root()
    mapp.create_index("root/mirror", indexconfig=dict(type=remote_index_info.type))
    mapp.create_and_login_user("user")
    mapp.create_index(
        "user/mirror", code=403, indexconfig=dict(type=remote_index_info.type)
    )
    xom.config.args.acl_mirror_index_create = None
    mapp.create_index("user/mirror", indexconfig=dict(type=remote_index_info.type))
    xom.config.args.acl_mirror_index_create = "user"
    mapp.create_index("user/mirror2", indexconfig=dict(type=remote_index_info.type))


def test_environment_config(makexom, mapp, monkeypatch, remote_index_info):
    import devpi_mirror_index_acl
    xom = makexom(plugins=[
        (devpi_mirror_index_acl, None)])
    assert xom.config.args.acl_mirror_index_create is None
    monkeypatch.setenv("DEVPISERVER_ACL_MIRROR_INDEX_CREATE", "root")
    xom = makexom(plugins=[
        (devpi_mirror_index_acl, None)])
    assert xom.config.args.acl_mirror_index_create == "root"
    mapp.login_root()
    mapp.create_index("root/mirror", indexconfig=dict(type=remote_index_info.type))


def test_config_file(makexom, mapp, remote_index_info, tmp_path):
    import devpi_mirror_index_acl
    import textwrap
    path = tmp_path.joinpath('devpi.yml')
    path.write_text(textwrap.dedent('''
        devpi-server:
          acl-mirror-index-create:
            - "root"
    '''))
    xom = makexom(
        opts=('-c', str(path)),
        plugins=[(devpi_mirror_index_acl, None)])
    assert xom.config.args.acl_mirror_index_create == ["root"]
    mapp.login_root()
    mapp.create_index("root/mirror", indexconfig=dict(type=remote_index_info.type))
