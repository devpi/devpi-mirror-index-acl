from devpi_server.model import ensure_acl_list
from devpi_server.model import get_principals
from pluggy import HookimplMarker


server_hookimpl = HookimplMarker("devpiserver")


@server_hookimpl
def devpiserver_add_parser_options(parser):
    parser.addoption(
        "--acl-mirror-index-create", type=str, metavar="SPEC",
        action="store", default=None,
        help="specify which users/groups may create mirror indexes.")


@server_hookimpl
def devpiserver_auth_denials(request, acl, user, stage):
    if request.method != 'PUT':
        return
    if request.context.index is None:
        return
    if request.json.get('type') != 'mirror':
        return
    xom = request.registry['xom']
    if xom.config.args.acl_mirror_index_create is None:
        return
    principals = get_principals(ensure_acl_list(
        xom.config.args.acl_mirror_index_create))
    result = []
    for (_, principal, permission) in acl:
        if permission != "index_create":
            continue
        if principal not in principals:
            result.append((principal, permission))
    return tuple(result)
