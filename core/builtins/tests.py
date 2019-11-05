from unittest import TestCase

from core.builtins.custom_tags import highlight_text


class TestStuff(TestCase):

    def test_highlight_text(self):
        span = '<span class="lite-highlight">'
        span_end = '</span>'

        actual_string = highlight_text('this is a sassy string', 'a')
        expected_string = 'this is ' + span + 'a' + span_end + ' s' + span + 'a' + span_end + 'ssy string'

        self.assertEqual(actual_string, expected_string)
