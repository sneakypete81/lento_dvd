import unittest
from hamcrest import assert_that, is_, is_not, contains_string
from mock import patch, call, Mock

from lento_dvd import lento_dvd

ACTIVE_ITEM = Mock()
ACTIVE_ITEM.get_active.return_value = True

INACTIVE_ITEM = Mock()
INACTIVE_ITEM.get_active.return_value = False

class TestLentoDvd(unittest.TestCase):
    def setUp(self):
        self.lento = lento_dvd.LentoDvd()

        patcher = patch("lento_dvd.eject.eject")
        self.eject_mock = patcher.start()
        self.addCleanup(patcher.stop)

    def test_speed_limit_can_be_set(self):
        self.lento.on_change_speed(ACTIVE_ITEM, 4)

        self.eject_mock.assert_called_once_with(cdspeed=4)

    def test_speed_limit_can_be_cleared(self):
        self.lento.on_change_speed(ACTIVE_ITEM, 32)
        self.lento.on_change_speed(ACTIVE_ITEM, lento_dvd.NO_LIMIT)

        expected_calls = [call(cdspeed=32), call(cdspeed=0)]
        assert_that(self.eject_mock.call_args_list, is_(expected_calls))

    def test_inactive_menu_item_is_ignored(self):
        # An 'activate' event is triggered when a menu item is deselected.
        # This event must be ignored.
        self.lento.on_change_speed(INACTIVE_ITEM, 2)
        self.lento.on_change_speed(ACTIVE_ITEM, 8)

        self.eject_mock.assert_called_once_with(cdspeed=8)

    @patch("lento_dvd.lento_dvd.gtk.main_quit")
    def test_speed_limit_is_removed_on_shutdown(self, _):
        self.lento.on_quit(None)

        self.eject_mock.assert_called_once_with(cdspeed=0)

    def test_off_icon_is_used_at_startup(self):
        assert_that(self.lento.indicator.get_icon(), contains_string("icon-off.svg"))

    def test_on_icon_is_used_when_speed_limit_is_set(self):
        self.lento.on_change_speed(ACTIVE_ITEM, 16)

        assert_that(self.lento.indicator.get_icon(), contains_string("icon-on.svg"))

    def test_on_icon_is_used_when_speed_limit_is_cleared(self):
        self.lento.on_change_speed(ACTIVE_ITEM, 64)
        self.lento.on_change_speed(ACTIVE_ITEM, lento_dvd.NO_LIMIT)

        assert_that(self.lento.indicator.get_icon(), contains_string("icon-off.svg"))

    @patch("lento_dvd.lento_dvd.glib.timeout_add_seconds")
    def test_timer_is_disabled_at_startup(self, timeout_mock):
        assert_that(self.lento.timer, is_(None))
        timeout_mock.assert_not_called()

    @patch("lento_dvd.lento_dvd.glib.timeout_add_seconds")
    def test_timer_is_enabled_when_speed_limit_is_set(self, timeout_mock):
        self.lento.on_change_speed(ACTIVE_ITEM, 1)

        assert_that(self.lento.timer, is_not(None))
        timeout_mock.assert_called_once_with(5, self.lento.change_speed, 1)

    @patch("lento_dvd.lento_dvd.glib.timeout_add_seconds")
    @patch("lento_dvd.lento_dvd.glib.source_remove")
    def test_timer_is_reenabled_when_speed_limit_is_set(self, remove_mock, timeout_mock):
        self.lento.on_change_speed(ACTIVE_ITEM, 4)
        first_timer = self.lento.timer
        self.lento.on_change_speed(ACTIVE_ITEM, 4)

        assert_that(self.lento.timer, is_not(None))
        expected_calls = [call(5, self.lento.change_speed, 4),
                          call(5, self.lento.change_speed, 4)]
        assert_that(timeout_mock.call_args_list, is_(expected_calls))
        remove_mock.assert_called_once_with(first_timer)

    @patch("lento_dvd.lento_dvd.glib.timeout_add_seconds")
    @patch("lento_dvd.lento_dvd.glib.source_remove")
    def test_timer_is_not_reenabled_when_speed_limit_is_cleared(self, remove_mock, timeout_mock):
        self.lento.on_change_speed(ACTIVE_ITEM, 8)
        first_timer = self.lento.timer
        self.lento.on_change_speed(ACTIVE_ITEM, lento_dvd.NO_LIMIT)

        assert_that(self.lento.timer, is_(None))
        timeout_mock.assert_called_once_with(5, self.lento.change_speed, 8)
        remove_mock.assert_called_once_with(first_timer)


        # import ipdb; ipdb.set_trace()

if __name__ == "__main__":
    unittest.main()
