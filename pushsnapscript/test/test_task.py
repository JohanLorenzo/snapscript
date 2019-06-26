import pytest

from scriptworker.exceptions import TaskVerificationError

from pushsnapscript.task import get_snap_channel, is_allowed_to_push_to_snap_store


@pytest.mark.parametrize('raises, scopes, expected', (
    (False, ['project:releng:snapcraft:firefox:candidate'], 'candidate'),
    (False, ['project:releng:snapcraft:firefox:beta'], 'beta'),
    (False, ['project:releng:snapcraft:firefox:esr'], 'esr'),
    (False, ['project:releng:snapcraft:firefox:mock'], 'mock'),
    (False, ['project:releng:snapcraft:firefox:beta', 'some:other:scope'], 'beta'),

    (True, ['project:releng:snapcraft:firefox:beta', 'project:releng:snapcraft:firefox:beta'], None),
    (True, ['project:releng:snapcraft:firefox:beta', 'project:releng:snapcraft:firefox:candidate'], None),
    (True, ['project:releng:snapcraft:firefox:edge'], None),
    (True, ['project:releng:snapcraft:firefox:stable'], None),
))
def test_get_snap_channel(raises, scopes, expected):
    task = {'scopes': scopes}
    if raises:
        with pytest.raises(TaskVerificationError):
            get_snap_channel(task)
    else:
        assert get_snap_channel(task) == expected



))
@pytest.mark.parametrize('channel, push_to_store, expected', (
    ('beta', True, True),
    ('candidate', True, True),
    ('esr/stable', True, True),
    ('esr/candidate', True, True),

    ('beta', False, False),
    ('candidate', False, False),
    ('esr/stable', False, False),
    ('esr/candidate', False, False),
    ('mock', True, False),
    ('mock', False, False),
))
def test_is_allowed_to_push_to_snap_store(channel, push_to_store, expected):
    config = {'push_to_store': push_to_store}
    assert is_allowed_to_push_to_snap_store(config, channel) == expected
