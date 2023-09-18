from data_handling.flavor_matcher import matches_flavor
from data_handling.parse_manifest import Asset


def asset_with_tags(old_asset, tags):
    return Asset(id=old_asset.id, flavor=old_asset.flavor, tags=tags, url=old_asset.url, filename=old_asset.filename,
                 mimetype=old_asset.mimetype, path=old_asset.path)


def asset_with_flavor(old_asset, flavor):
    return Asset(id=old_asset.id, flavor=flavor, tags=old_asset.tags, url=old_asset.url, filename=old_asset.filename,
                 mimetype=old_asset.mimetype, path=old_asset.path)


def asset_with_tags_and_flavor(old_asset, tags, flavor):
    return Asset(id=old_asset.id, flavor=flavor, tags=tags, url=old_asset.url, filename=old_asset.filename,
                 mimetype=old_asset.mimetype, path=old_asset.path)


def filter_by_flavor(assets, flavor):
    return [asset for asset in assets if matches_flavor(asset.flavor, [flavor])]


def set_tags(assets, tags):
    return [asset_with_tags(asset, tags) for asset in assets]


def set_flavor(assets, flavor):
    return [asset_with_flavor(asset, flavor) for asset in assets]


def is_single_stream(tracks):
    if len(tracks) == 1:
        return True
    return all([track.flavor == tracks[0].flavor for track in tracks])
