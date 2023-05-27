from unittest import TestCase
from maya import cmds


class TestBatch(TestCase):
    def test_batch(self):
        maya_version = int(cmds.about(q=True, majorVersion=True))
        self.assertEqual(maya_version, 2023)
        