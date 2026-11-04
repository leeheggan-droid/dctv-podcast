import unittest
from build_feed import mirror


def feed(guid='old', url='https://example.org/old.mp3', extra=''):
    return f'<rss><channel><title>DC TV with Lee Heggan</title><item><guid>{guid}</guid><pubDate>date</pubDate><enclosure url="{url}" length="123" type="audio/mpeg"/></item>{extra}</channel></rss>'.encode()


class MirrorTests(unittest.TestCase):
    def test_preserves_existing_and_adds_new_episode(self):
        extra = '<item><guid>new</guid><pubDate>new date</pubDate><enclosure url="https://example.org/new.mp3" length="456" type="audio/mpeg"/></item>'
        self.assertIn(b'<guid>new</guid>', mirror(feed(), feed(extra=extra)))

    def test_rejects_changed_identity(self):
        with self.assertRaisesRegex(ValueError, 'identity'):
            mirror(feed(), feed(guid='replacement'))

    def test_rejects_changed_audio(self):
        with self.assertRaisesRegex(ValueError, 'audio'):
            mirror(feed(), feed(url='https://example.org/replacement.mp3'))

    def test_rejects_empty_feed(self):
        with self.assertRaisesRegex(ValueError, 'Empty'):
            mirror(feed(), b'<rss><channel/></rss>')


if __name__ == '__main__':
    unittest.main()
